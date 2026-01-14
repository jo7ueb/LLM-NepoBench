import argparse
import json
import os
import re
import shutil
import subprocess
import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

import pandas as pd
import yaml
from openai import OpenAI


WORKDIR = "./_work"

RUNNER_SERVICE = {
    "python": "py-runner",
    "typescript": "ts-runner",
    "go": "go-runner",
}

SOLUTION_FILENAME = {
    "python": "solution.py",
    "typescript": "solution.ts",
    "go": "solution.go",
}

DEFAULT_BASE_URL = {
    "lmstudio": "http://localhost:1234/v1",
    "openrouter": "https://openrouter.ai/api/v1",
    "openai": "https://api.openai.com/v1",
}


@dataclass
class Problem:
    id: str
    lang: str
    prompt: str
    tests: Dict[str, str]


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--provider", required=True, choices=["lmstudio", "openrouter", "openai"])
    p.add_argument("--model", required=True)
    p.add_argument("--base-url", default=None)
    p.add_argument("--api-key", default=None)

    p.add_argument("--langs", default="python,typescript,go", help="comma-separated, e.g. python,go")
    p.add_argument("--runs", type=int, default=3)
    p.add_argument("--temperature", type=float, default=0.1)
    p.add_argument("--max-tokens", type=int, default=1024)
    p.add_argument("--docker-timeout", type=int, default=45, help="seconds for docker test run")
    p.add_argument("--out", default="results.csv")
    return p.parse_args()


def build_client(args: argparse.Namespace) -> OpenAI:
    provider = args.provider.lower()
    base_url = args.base_url or DEFAULT_BASE_URL[provider]

    if provider == "lmstudio":
        # LM Studio はダミーキーでも通ることが多い
        api_key = args.api_key or os.getenv("LMSTUDIO_API_KEY", "lm-studio")
        return OpenAI(base_url=base_url, api_key=api_key)

    if provider == "openrouter":
        api_key = args.api_key or os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise RuntimeError("OPENROUTER_API_KEY が未設定です（または --api-key を指定してください）")
        return OpenAI(base_url=base_url, api_key=api_key)

    if provider == "openai":
        api_key = args.api_key or os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY が未設定です（または --api-key を指定してください）")
        return OpenAI(base_url=base_url, api_key=api_key)

    raise ValueError(f"Unknown provider: {provider}")


_CODE_FENCE_RE = re.compile(r"```(?:[a-zA-Z0-9_+-]*)\n(.*?)```", re.DOTALL)


def extract_code(text: str) -> str:
    """
    生成物に ``` が含まれる場合は最初のコードブロックを採用。
    無い場合は全文を採用。
    """
    if not text:
        return ""
    m = _CODE_FENCE_RE.search(text)
    if m:
        return m.group(1).strip() + "\n"
    return text.strip() + "\n"


def reset_workdir() -> None:
    if os.path.exists(WORKDIR):
        shutil.rmtree(WORKDIR)
    os.makedirs(WORKDIR, exist_ok=True)


def write_files(tree: Dict[str, str]) -> None:
    for relpath, content in tree.items():
        abspath = os.path.join(WORKDIR, relpath)
        os.makedirs(os.path.dirname(abspath), exist_ok=True)
        with open(abspath, "w", encoding="utf-8") as f:
            f.write(content)


def docker_run(service: str, timeout_s: int) -> tuple[int, str]:
    """
    docker compose run --rm <service>
    """
    try:
        p = subprocess.run(
            ["docker", "compose", "run", "--rm", service],
            capture_output=True,
            text=True,
            timeout=timeout_s,
        )
        out = (p.stdout or "") + (p.stderr or "")
        return p.returncode, out
    except subprocess.TimeoutExpired as e:
        out = (e.stdout or "") + (e.stderr or "")
        return 124, f"[TIMEOUT] docker run exceeded {timeout_s}s\n" + out
    except Exception as e:
        return 125, f"[ERROR] docker invocation failed: {e}"


def parse_test_report(lang: str) -> Tuple[int, int, int]:
    """
    テストレポートをパースして (passed, failed, total) を返す。
    部分点評価用。レポートが見つからない場合は (0, 0, 0) を返す。
    """
    report_path = os.path.join(WORKDIR, ".report.json")

    if lang == "python" and os.path.exists(report_path):
        try:
            with open(report_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            summary = data.get("summary", {})
            passed = summary.get("passed", 0)
            failed = summary.get("failed", 0)
            error = summary.get("error", 0)
            total = summary.get("total", passed + failed + error)
            return passed, failed + error, total
        except (json.JSONDecodeError, KeyError):
            pass

    if lang == "typescript" and os.path.exists(report_path):
        try:
            with open(report_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            # vitest JSON format: { testResults: [{ assertionResults: [...] }] }
            passed = 0
            failed = 0
            for test_file in data.get("testResults", []):
                for assertion in test_file.get("assertionResults", []):
                    if assertion.get("status") == "passed":
                        passed += 1
                    else:
                        failed += 1
            total = passed + failed
            if total > 0:
                return passed, failed, total
        except (json.JSONDecodeError, KeyError):
            pass

    if lang == "go" and os.path.exists(report_path):
        try:
            with open(report_path, "r", encoding="utf-8") as f:
                # go test -json は各行が独立したJSONオブジェクト
                passed = 0
                failed = 0
                seen_tests = set()
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        event = json.loads(line)
                        action = event.get("Action")
                        test_name = event.get("Test")
                        # テスト関数単位でカウント（サブテストは親に含める）
                        if test_name and "/" not in test_name:
                            if action == "pass" and test_name not in seen_tests:
                                passed += 1
                                seen_tests.add(test_name)
                            elif action == "fail" and test_name not in seen_tests:
                                failed += 1
                                seen_tests.add(test_name)
                    except json.JSONDecodeError:
                        continue
                total = passed + failed
                if total > 0:
                    return passed, failed, total
        except IOError:
            pass

    return 0, 0, 0


def calculate_score(rc: int, lang: str) -> Tuple[int, int, int, int]:
    """
    部分点スコアを計算する。
    Returns: (score, passed, failed, total)
    - 全テスト通過: 100点
    - 部分通過: (passed / total) * 100
    - レポートがない場合: 従来どおり0/100
    """
    passed, failed, total = parse_test_report(lang)

    if total > 0:
        # 部分点計算
        score = round((passed / total) * 100)
        return score, passed, failed, total

    # 従来どおりの0/100評価
    if rc == 0:
        return 100, 1, 0, 1
    return 0, 0, 1, 1


def load_problems(selected_langs: List[str]) -> List[Problem]:
    problems: List[Problem] = []
    for lang in selected_langs:
        path = os.path.join("problems", f"{lang}.yaml")
        if not os.path.exists(path):
            print(f"[WARN] not found: {path} (skip)")
            continue
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or []
        for item in data:
            problems.append(
                Problem(
                    id=str(item["id"]),
                    lang=str(item["lang"]).lower(),
                    prompt=str(item["prompt"]),
                    tests=dict(item.get("tests", {})),
                )
            )
    return problems


def main() -> None:
    args = parse_args()
    selected_langs = [s.strip().lower() for s in args.langs.split(",") if s.strip()]
    client = build_client(args)

    problems = load_problems(selected_langs)
    if not problems:
        raise RuntimeError("問題がロードできませんでした。problems/*.yaml を確認してください。")

    rows: List[Dict[str, Any]] = []

    print(f"Provider: {args.provider}")
    print(f"Base URL: {args.base_url or DEFAULT_BASE_URL[args.provider]}")
    print(f"Model:    {args.model}")
    print(f"Langs:    {selected_langs}")
    print(f"Runs:     {args.runs}")
    print("")

    for prob in problems:
        if prob.lang not in RUNNER_SERVICE:
            print(f"[WARN] unsupported runner for lang={prob.lang}, skip {prob.id}")
            continue

        service = RUNNER_SERVICE[prob.lang]
        sol_name = SOLUTION_FILENAME[prob.lang]

        for run_idx in range(1, args.runs + 1):
            reset_workdir()
            write_files(prob.tests)

            # Go は go.mod が必要
            if prob.lang == "go":
                write_files({"go.mod": "module bench\n\ngo 1.22\n"})

            # LLM 呼び出し
            t0 = time.time()
            resp = client.chat.completions.create(
                model=args.model,
                messages=[
                    {"role": "system", "content": f"You are an expert {prob.lang} developer. Output code only."},
                    {"role": "user", "content": prob.prompt},
                ],
                temperature=args.temperature,
                max_tokens=args.max_tokens,
            )
            t1 = time.time()

            content = resp.choices[0].message.content or ""
            code = extract_code(content)
            write_files({sol_name: code})

            # Docker 内でテスト
            rc, log = docker_run(service, timeout_s=args.docker_timeout)
            score, tests_passed, tests_failed, tests_total = calculate_score(rc, prob.lang)
            all_passed = (rc == 0)

            rows.append(
                {
                    "problem_id": prob.id,
                    "lang": prob.lang,
                    "run": run_idx,
                    "score": score,
                    "passed": all_passed,
                    "tests_passed": tests_passed,
                    "tests_failed": tests_failed,
                    "tests_total": tests_total,
                    "exit_code": rc,
                    "llm_seconds": round(t1 - t0, 3),
                    "docker_timeout_s": args.docker_timeout,
                    "log_head": log[:2000],  # ログ長暴走を防ぐ
                }
            )

            status = "PASS" if all_passed else f"PARTIAL({tests_passed}/{tests_total})" if tests_passed > 0 else "FAIL"
            print(f"[{prob.lang}] {prob.id} run {run_idx}/{args.runs} -> {status} score={score} (rc={rc})")

    df = pd.DataFrame(rows)
    df.to_csv(args.out, index=False, encoding="utf-8")
    print("")
    print(f"Saved: {args.out}")

    # サマリ表示
    summary = (
        df.groupby(["lang", "problem_id"])
        .agg(
            pass_rate=("passed", "mean"),
            avg_score=("score", "mean"),
            std_score=("score", "std"),
            avg_llm_seconds=("llm_seconds", "mean"),
        )
        .reset_index()
        .sort_values(["lang", "problem_id"])
    )
    print("\n=== Summary (per problem) ===")
    print(summary.to_string(index=False))

    lang_summary = (
        df.groupby(["lang"])
        .agg(
            pass_rate=("passed", "mean"),
            avg_score=("score", "mean"),
            std_score=("score", "std"),
            avg_llm_seconds=("llm_seconds", "mean"),
        )
        .reset_index()
        .sort_values(["lang"])
    )
    print("\n=== Summary (per language) ===")
    print(lang_summary.to_string(index=False))


if __name__ == "__main__":
    main()

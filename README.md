# local-llm / llm-bench (MVP)
ローカルLLM（LM Studio など）と商用LLM（OpenRouter など）を、同一の問題・同一のテストで比較するための最小ベンチです。

- LLMが生成したコードを ./_work に書き出す
- Dockerコンテナ（言語ごとのランナー）でテスト実行
- PASS=100 / FAIL=0 としてCSVに保存
- --runs N 回の繰り返しで安定性（合格率・ブレ）を測れます

※MVPでは Python / TypeScript / Go の3言語のみ対応。

------------------------------------------------------------
目次
------------------------------------------------------------
1. 前提条件
2. リポジトリ構成
3. 初回セットアップ
4. Dockerイメージのビルド
5. ローカルLLM（LM Studio）で実行
6. 商用LLM（OpenRouter）で実行
7. 結果の見方
8. よくあるトラブルと対処
9. 問題の追加方法

------------------------------------------------------------
1. 前提条件
------------------------------------------------------------
必須:
- Docker + Docker Compose が動作すること
- Python 3.10+（ローカルで bench.py を実行）

推奨:
- WSL2（Windowsの場合）+ Docker Desktop

------------------------------------------------------------
2. リポジトリ構成
------------------------------------------------------------
bench/
  bench.py
  docker-compose.yml
  README.md
  problems/
    python.yaml
    typescript.yaml
    go.yaml
  runners/
    python/
      Dockerfile
      run.sh
    typescript/
      Dockerfile
      run.sh
    go/
      Dockerfile
      run.sh
  _work/   ← 実行時に bench.py が一時ファイルを置く（自動生成）

------------------------------------------------------------
3. 初回セットアップ
------------------------------------------------------------
このディレクトリで以下を実行。

(venv推奨)

  python -m venv .venv
  source .venv/bin/activate   # Windows PowerShellの場合は適宜読み替え
  pip install -U pip
  pip install openai pyyaml pandas

------------------------------------------------------------
4. Dockerイメージのビルド
------------------------------------------------------------
4.1 CRLF対策（WSL/Windows環境で推奨）
run.sh が Windows 改行（CRLF）だと、コンテナ内で ^M エラーになることがあります。
念のため一度だけ実行しておくと安全です。

  sed -i 's/\r$//' runners/python/run.sh runners/typescript/run.sh runners/go/run.sh

4.2 ビルド
  docker compose build

うまくいかない場合（先に pull してみる）
  docker pull python:3.12-slim
  docker pull node:20-slim
  docker pull golang:1.22-alpine
  docker compose build

------------------------------------------------------------
5. ローカルLLM（LM Studio）で実行
------------------------------------------------------------
5.1 LM Studio側の準備
LM Studioで対象モデルをロードし、OpenAI互換サーバを起動します。

- Base URL 例: http://localhost:1234/v1

5.2 実行（全部の言語を回す）
  python bench.py \
    --provider lmstudio \
    --model local-model \
    --base-url http://localhost:1234/v1 \
    --runs 3 \
    --out results_local.csv

言語を絞る例（Pythonだけ）
  python bench.py \
    --provider lmstudio \
    --model local-model \
    --base-url http://localhost:1234/v1 \
    --langs python \
    --runs 5 \
    --out results_py_only.csv

------------------------------------------------------------
6. 商用LLM（OpenRouter）で実行
------------------------------------------------------------
6.1 OpenRouter APIキーを設定
  export OPENROUTER_API_KEY="あなたのキー"

6.2 実行
  python bench.py \
    --provider openrouter \
    --model anthropic/claude-3.5-sonnet \
    --runs 3 \
    --out results_openrouter.csv

------------------------------------------------------------
7. 結果の見方
------------------------------------------------------------
--out で指定したCSVに全ログが出ます。

7.1 CSVの主な列
- problem_id : 問題ID
- lang : 言語（python/typescript/go）
- run : 何回目の試行か（1..N）
- score : 100（PASS）または0（FAIL）
- passed : true/false
- exit_code : Docker内テストの終了コード（0が成功）
- llm_seconds : LLM応答時間（スループット目的ではなく参考値）
- log_head : テストログの先頭（最大2000文字）

7.2 bench.py の標準出力サマリ
実行後に
- 問題ごとの pass_rate / std_score
- 言語ごとの pass_rate / std_score
が表示されます。

安定性（ブレ）の読み方:
- pass_rate が 1.0 に近いほど「一発で成功しやすい」
- std_score が大きいほど「成功したり失敗したりで不安定」

------------------------------------------------------------
8. よくあるトラブルと対処
------------------------------------------------------------
8.1 error getting credentials / Docker Hub から pull できない
WSLでDocker認証が壊れていることがあります。
まずは以下で ~/.docker/config.json を最小化して回復するケースが多いです。

  cp ~/.docker/config.json ~/.docker/config.json.bak
  cat > ~/.docker/config.json <<'JSON'
  {
    "auths": {}
  }
  JSON
  docker logout
  docker pull node:20-slim

それでもダメなら Docker Desktop と WSL の再起動:
(PowerShell)
  wsl --shutdown

8.2 chmod: Operation not permitted
Dockerfile内で USER 切替後に chmod すると起きます。
本ベンチは Dockerfile 側で COPY --chmod=755 + ENTRYPOINT を使う構成に寄せています。

8.3 ^M: bad interpreter（run.shが実行できない）
run.sh が CRLF 改行の可能性。
4.1 の CRLF対策を実行してください。

8.4 生成コードが長すぎてテストが走る前に詰まる
--max-tokens を下げる、または問題文を短くする。
問題ごとに期待する出力フォーマット（単一ファイルのみ等）を明示してください。

8.5 Docker内でテストがタイムアウトする
デフォルトは --docker-timeout 45 秒です。延ばす例:

  python bench.py ... --docker-timeout 120

------------------------------------------------------------
9. 問題の追加方法
------------------------------------------------------------
problems/<lang>.yaml に問題を追加します。

9.1 YAMLの基本形
  - id: unique_id
    lang: python
    prompt: |
      ここにプロンプト
    tests:
      tests/test_solution.py: |
        ここにテストコード

9.2 重要ポイント
- lang は python / typescript / go のいずれか
- 生成コードは固定ファイル名として書き出されます:
  - python: _work/solution.py
  - typescript: _work/solution.ts
  - go: _work/solution.go（加えて _work/go.mod が自動生成されます）
- tests のキーは workdir直下からの相対パス（例: tests/test_solution.py）

------------------------------------------------------------
おすすめ運用
------------------------------------------------------------
- 最初は --runs 3 で荒く比較
- 良さげなモデルが見つかったら --runs 10 でブレを確認
- Python中心なら Python問題を実務寄りに増やすと効果が大きい
  - FastAPI（依存注入/例外処理）
  - SQLAlchemy（N+1回避）
  - asyncio（ロック/競合）
  - データ変換（型ヒント/データクラス）

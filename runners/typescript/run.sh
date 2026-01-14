#!/usr/bin/env bash
set -euo pipefail

# /work に
# /work/solution.ts
# /work/tests/solution.test.ts
# を置く想定

# vitest を JSON レポート出力で実行
# --no-cache でキャッシュを無効化（権限問題を回避）
cd /work
vitest run --no-cache --reporter=json --outputFile=.report.json 2>&1 || exit_code=$?

# 終了コードを返す
exit ${exit_code:-0}

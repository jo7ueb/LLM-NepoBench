#!/usr/bin/env bash
set -euo pipefail

# /work に
# /work/solution.ts
# /work/tests/solution.test.ts
# を置く想定

cd /work

# vitest を実行（通常出力 + JSON レポート）
vitest run --no-cache --reporter=verbose --reporter=json --outputFile=.report.json 2>&1 || exit_code=$?

# 終了コードを返す
exit ${exit_code:-0}

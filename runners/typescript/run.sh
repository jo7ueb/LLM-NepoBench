#!/usr/bin/env bash
set -euo pipefail

# /work に
# /work/solution.ts
# /work/tests/solution.test.ts
# を置く想定

# vitest を JSON レポート出力で実行（部分点評価用）
vitest run --reporter=json --outputFile=/work/.report.json || exit_code=$?

# 終了コードを返す
exit ${exit_code:-0}

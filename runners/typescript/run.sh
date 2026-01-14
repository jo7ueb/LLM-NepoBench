#!/usr/bin/env bash
set -euo pipefail

# /work に
# /work/solution.ts
# /work/tests/solution.test.ts
# を置く想定

# キャッシュディレクトリを /tmp に設定（権限問題を回避）
export VITEST_CACHE_DIR=/tmp/.vitest
export VITE_CACHE_DIR=/tmp/.vite

# /tmp にキャッシュディレクトリを作成
mkdir -p /tmp/.vitest /tmp/.vite

# vitest を JSON レポート出力で実行（部分点評価用）
# --config で設定ファイルを指定（キャッシュディレクトリ設定）
vitest run --config /runner/vitest.config.ts --reporter=json --outputFile=/work/.report.json 2>&1 || exit_code=$?

# 終了コードを返す
exit ${exit_code:-0}

#!/usr/bin/env bash
set -euo pipefail

# /work には bench.py が問題ごとに生成したファイルが置かれる想定
# 例:
# /work/solution.py
# /work/tests/test_solution.py

# pytest-json-report で結果をJSONに出力（部分点評価用）
# 終了コードは pytest が返す（0=全て通過, 1=一部失敗, etc）
python -m pytest -q --json-report --json-report-file=/work/.report.json || exit_code=$?

# 終了コードを返す
exit ${exit_code:-0}

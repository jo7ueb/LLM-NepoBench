#!/usr/bin/env bash
set -euo pipefail

# /work には bench.py が問題ごとに生成したファイルが置かれる想定
# 例:
# /work/solution.py
# /work/tests/test_solution.py

python -m pytest -q

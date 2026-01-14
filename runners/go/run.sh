#!/bin/sh
set -eu

# /work に go.mod, solution.go, *_test.go を置く想定
# JSON出力で部分点評価に対応
go test ./... -count=1 -json > /work/.report.json 2>&1 || exit_code=$?

exit ${exit_code:-0}

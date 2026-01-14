#!/bin/sh
set -eu

# /work に go.mod, solution.go, *_test.go を置く想定
go test ./... -count=1

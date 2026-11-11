#!/bin/sh
set -eu

cd "$(dirname "$0")"
repo=$(awk '$2 == "papermerge-source:" {print $3}' requirements.txt)
revision=$(awk '$2 == "papermerge-source:" {print $4}' requirements.txt)
scratch=$(mktemp -d)
trap 'rm -rf "$scratch"' EXIT

git init -q "$scratch"
git -C "$scratch" fetch -q --depth=1 "$repo" "$revision"
git -C "$scratch" checkout -q --detach FETCH_HEAD
test "$(git -C "$scratch" rev-parse HEAD)" = "$revision"

PYTHONPATH="$scratch" python demo.py

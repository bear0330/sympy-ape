#!/bin/sh
set -eu

project_root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
classes=$(mktemp -d)
trap 'rm -rf "$classes"' EXIT

javac --release 17 -d "$classes" \
  "$project_root/src/main/java/apebind/generated/sympy_ape/"*.java \
  "$project_root/tests/SympySmoke.java"
java -cp "$classes:$project_root/src/main/resources" SympySmoke

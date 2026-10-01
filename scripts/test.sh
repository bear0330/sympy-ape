#!/bin/sh
set -eu

repository_root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)

python3 "$repository_root/tests/test_sympy_com.py"
"$repository_root/bindings/node/scripts/test.sh"
"$repository_root/bindings/java/scripts/test.sh"

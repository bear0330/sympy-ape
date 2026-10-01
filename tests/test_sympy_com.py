# SPDX-License-Identifier: MIT

from __future__ import annotations

import errno
import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SYMPY = ROOT / "sympy.com"


class SympyComTests(unittest.TestCase):
    def run_sympy(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        command = [str(SYMPY), *arguments]
        try:
            return subprocess.run(
                command,
                check=False,
                cwd=ROOT,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
            )
        except OSError as exc:
            if exc.errno != errno.ENOEXEC:
                raise
            return subprocess.run(
                ["/bin/sh", "-c", 'exec "$0" "$@"', *command],
                check=False,
                cwd=ROOT,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
            )

    def test_version_json(self) -> None:
        result = self.run_sympy("version")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["result"], "1.14.0")

    def test_integrate_json_and_text(self) -> None:
        parsed = json.loads(self.run_sympy("integrate", "sin(x)").stdout)
        text = self.run_sympy("integrate", "--text", "sin(x)")

        self.assertEqual(parsed["result"], "-cos(x)")
        self.assertIn("cos", parsed["latex"])
        self.assertEqual(text.stdout.strip(), "-cos(x)")

    def test_leading_dash_expression(self) -> None:
        parsed = json.loads(self.run_sympy("diff", "-x**2").stdout)

        self.assertEqual(parsed["result"], "-2*x")

    def test_bad_expression_exits_nonzero(self) -> None:
        result = self.run_sympy("eval", "not_a_symbol")

        self.assertEqual(result.returncode, 1)
        self.assertIn("NameError", result.stderr)


if __name__ == "__main__":
    unittest.main()

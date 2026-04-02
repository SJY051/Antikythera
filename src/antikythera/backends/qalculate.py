from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

DEFAULT_QALC_PATHS = [
  Path(r"C:\Program Files\Qalculate\qalc.exe"),
  Path(r"C:\Program Files (x86)\Qalculate\qalc.exe"),
]


def find_qalc() -> str | None:
  resolved = shutil.which("qalc")
  if resolved:
    return resolved

  for candidate in DEFAULT_QALC_PATHS:
    if candidate.exists():
      return str(candidate)

  return None


def qalculate_compute(
  expression: str,
  *,
  timeout_ms: int = 3000,
  terse: bool = True,
) -> dict[str, str | int | bool]:
  binary = find_qalc()
  if binary is None:
    raise FileNotFoundError("qalc executable not found")

  args = [binary]
  if terse:
    args.append("--terse")
  args.extend(["--time", str(timeout_ms), expression])

  completed = subprocess.run(
    args,
    capture_output=True,
    text=True,
    encoding="utf-8",
    errors="replace",
    check=False,
  )

  stdout = completed.stdout.strip()
  stderr = completed.stderr.strip()
  ok = completed.returncode == 0
  result = stdout if stdout else stderr

  return {
    "expression": expression,
    "backend": "qalculate",
    "binary": binary,
    "ok": str(ok).lower(),
    "exit_code": completed.returncode,
    "result": result,
    "stderr": stderr,
  }

from __future__ import annotations

import json
import subprocess
import sys
from collections.abc import Callable
from typing import Any

from .errors import format_tool_error

def run_with_timeout(
  func: Callable[..., Any],
  *args: Any,
  timeout_ms: int = 5000,
  **kwargs: Any,
) -> Any:
  payload = json.dumps(
    {
      "args": args,
      "kwargs": kwargs,
    },
    ensure_ascii=False,
  )

  try:
    completed = subprocess.run(
      [sys.executable, "-m", "antikythera.worker", func.__name__, payload],
      capture_output=True,
      text=True,
      encoding="utf-8",
      errors="replace",
      timeout=timeout_ms / 1000,
      check=False,
    )
  except subprocess.TimeoutExpired as exc:
    raise TimeoutError(f"operation timed out after {timeout_ms}ms") from exc

  if completed.returncode != 0:
    stdout = completed.stdout.strip()
    if stdout:
      try:
        payload = json.loads(stdout)
      except json.JSONDecodeError:
        payload = None
      if payload and payload.get("ok") is False:
        error = payload["error"]
        raise RuntimeError(format_tool_error(error["type"], error["message"]))

    message = completed.stderr.strip() or stdout or f"worker exited with code {completed.returncode}"
    raise RuntimeError(message)

  payload = json.loads(completed.stdout)
  return payload["result"]

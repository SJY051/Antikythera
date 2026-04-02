from __future__ import annotations

import json
import sys
from typing import Any

from .core import (
  differentiate_expression,
  evaluate_expression,
  integrate_expression,
  matrix_compute,
  numeric_compute,
  solve_equation,
  unit_convert,
)

FUNCTIONS = {
  "evaluate_expression": evaluate_expression,
  "solve_equation": solve_equation,
  "differentiate_expression": differentiate_expression,
  "integrate_expression": integrate_expression,
  "matrix_compute": matrix_compute,
  "unit_convert": unit_convert,
  "numeric_compute": numeric_compute,
}


def main() -> None:
  if len(sys.argv) != 3:
    raise SystemExit("usage: python -m antikythera.worker <function_name> <json-payload>")

  function_name = sys.argv[1]
  payload = json.loads(sys.argv[2])
  func = FUNCTIONS.get(function_name)
  if func is None:
    raise SystemExit(f"unknown function: {function_name}")

  try:
    args = payload.get("args", [])
    kwargs = payload.get("kwargs", {})
    result = func(*args, **kwargs)
    print(json.dumps({"ok": True, "result": result}, ensure_ascii=False))
  except Exception as exc:
    print(
      json.dumps(
        {
          "ok": False,
          "error": {
            "type": exc.__class__.__name__,
            "message": str(exc),
          },
        },
        ensure_ascii=False,
      )
    )
    raise SystemExit(1)


if __name__ == "__main__":
  main()

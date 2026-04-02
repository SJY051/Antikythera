from __future__ import annotations


def format_tool_error(error_type: str, message: str) -> str:
  lowered = message.lower()

  if error_type in {"SyntaxError", "TokenError"} or "invalid syntax" in lowered:
    return "parse_error: expression syntax could not be parsed. Try explicit multiplication like 2*x and exponent syntax like x**2."

  if "could not parse" in lowered or "sympify" in lowered:
    return "parse_error: expression could not be normalized. Try a simpler mathematical form with explicit operators."

  if "dimensionalityerror" in lowered or "cannot convert from" in lowered:
    return "dimension_mismatch: the requested unit conversion is not dimensionally valid."

  if "operation timed out" in lowered:
    return f"timeout: {message}"

  return f"{error_type}: {message}"

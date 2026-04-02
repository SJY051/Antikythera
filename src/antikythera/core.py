from __future__ import annotations

from typing import Any

import numpy as np
from mpmath import mp
from pint import UnitRegistry
from sympy import Matrix, Symbol, diff, integrate, lambdify, nsimplify, simplify, solve

from .parsing import parse_equation, parse_expression

ureg = UnitRegistry()


def _stringify(value: Any) -> Any:
  if isinstance(value, dict):
    return {str(key): _stringify(val) for key, val in value.items()}
  if isinstance(value, (list, tuple)):
    return [_stringify(item) for item in value]
  return str(value)


def _symbol_map(substitutions: dict[str, Any] | None) -> dict[Symbol, Any]:
  if not substitutions:
    return {}
  return {Symbol(name): value for name, value in substitutions.items()}


def evaluate_expression(
  expression: str,
  substitutions: dict[str, Any] | None = None,
  *,
  numeric: bool = False,
  precision: int = 50,
) -> dict[str, Any]:
  parsed = parse_expression(expression)
  substituted = parsed.expr.subs(_symbol_map(substitutions))
  simplified = simplify(substituted)
  payload: dict[str, Any] = {
    "backend": "sympy",
    "expression": expression,
    "normalized_input": parsed.normalized,
    "symbolic": str(simplified),
  }

  if numeric:
    mp.dps = precision
    payload["numeric"] = str(simplified.evalf(precision))

  return payload


def solve_equation(
  equation: str,
  symbol: str,
  substitutions: dict[str, Any] | None = None,
) -> dict[str, Any]:
  parsed = parse_equation(equation)
  eq = parsed.equation.subs(_symbol_map(substitutions))
  sym = Symbol(symbol)
  solutions = solve(eq, sym)
  return {
    "backend": "sympy",
    "equation": str(eq),
    "normalized_input": parsed.normalized,
    "symbol": symbol,
    "solutions": _stringify(solutions),
  }


def differentiate_expression(
  expression: str,
  symbol: str,
  *,
  order: int = 1,
) -> dict[str, Any]:
  parsed = parse_expression(expression)
  sym = Symbol(symbol)
  derivative = diff(parsed.expr, sym, order)
  return {
    "backend": "sympy",
    "expression": expression,
    "normalized_input": parsed.normalized,
    "symbol": symbol,
    "order": order,
    "result": str(simplify(derivative)),
  }


def integrate_expression(
  expression: str,
  symbol: str,
  *,
  lower_bound: str | None = None,
  upper_bound: str | None = None,
) -> dict[str, Any]:
  parsed = parse_expression(expression)
  sym = Symbol(symbol)

  if lower_bound is not None and upper_bound is not None:
    lower = parse_expression(lower_bound)
    upper = parse_expression(upper_bound)
    result = integrate(parsed.expr, (sym, lower.expr, upper.expr))
    mode = "definite"
  else:
    lower = None
    upper = None
    result = integrate(parsed.expr, sym)
    mode = "indefinite"

  return {
    "backend": "sympy",
    "expression": expression,
    "normalized_input": parsed.normalized,
    "symbol": symbol,
    "mode": mode,
    "normalized_lower_bound": lower.normalized if lower is not None else None,
    "normalized_upper_bound": upper.normalized if upper is not None else None,
    "result": str(simplify(result)),
  }


def matrix_compute(
  operation: str,
  matrix: list[list[float]],
  other_matrix: list[list[float]] | None = None,
) -> dict[str, Any]:
  mat = Matrix(matrix)

  if operation == "determinant":
    result: Any = mat.det()
  elif operation == "inverse":
    result = mat.inv()
  elif operation == "transpose":
    result = mat.T
  elif operation == "eigenvalues":
    result = mat.eigenvals()
  elif operation == "add":
    if other_matrix is None:
      raise ValueError("other_matrix is required for add")
    result = mat + Matrix(other_matrix)
  elif operation == "multiply":
    if other_matrix is None:
      raise ValueError("other_matrix is required for multiply")
    result = mat * Matrix(other_matrix)
  else:
    raise ValueError(f"unsupported matrix operation: {operation}")

  if isinstance(result, Matrix):
    normalized: Any = result.tolist()
  else:
    normalized = _stringify(result)

  return {
    "backend": "sympy",
    "operation": operation,
    "result": normalized,
  }


def unit_convert(value: float, from_unit: str, to_unit: str) -> dict[str, Any]:
  quantity = value * ureg(from_unit)
  converted = quantity.to(to_unit)
  return {
    "backend": "pint",
    "input": f"{value} {from_unit}",
    "output": f"{converted.magnitude} {converted.units}",
    "magnitude": converted.magnitude,
    "unit": str(converted.units),
  }


def numeric_compute(
  expression: str,
  variable: str,
  start: float,
  end: float,
  *,
  samples: int = 100,
) -> dict[str, Any]:
  parsed = parse_expression(expression)
  sym = Symbol(variable)
  fn = lambdify(sym, parsed.expr, modules=["numpy"])
  xs = np.linspace(start, end, samples)
  ys = fn(xs)
  return {
    "backend": "numpy",
    "expression": expression,
    "normalized_input": parsed.normalized,
    "variable": variable,
    "start": start,
    "end": end,
    "samples": samples,
    "min": float(np.min(ys)),
    "max": float(np.max(ys)),
    "mean": float(np.mean(ys)),
    "sample_points": [
      {"x": float(x), "y": float(y)}
      for x, y in zip(xs[:5], ys[:5], strict=False)
    ],
  }

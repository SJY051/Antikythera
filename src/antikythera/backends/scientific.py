from __future__ import annotations

from typing import Any

from scipy.optimize import minimize_scalar, root_scalar
from sympy import Symbol, lambdify

from ..parsing import parse_expression


def numeric_solve(
  expression: str,
  symbol: str,
  bracket: list[float] | None = None,
  initial_guess: float | None = None,
  method: str = "brentq",
) -> dict[str, Any]:
  parsed = parse_expression(expression)
  sym = Symbol(symbol)
  fn = lambdify(sym, parsed.expr, modules=["numpy"])

  if bracket is not None:
    if len(bracket) != 2:
      raise ValueError("bracket must contain exactly two numeric values")
    result = root_scalar(fn, bracket=tuple(bracket), method=method)
  elif initial_guess is not None:
    result = root_scalar(fn, x0=initial_guess, x1=initial_guess + 1e-3, method="secant")
  else:
    raise ValueError("either bracket or initial_guess is required")

  if not result.converged:
    raise RuntimeError("numeric root finding did not converge")

  return {
    "backend": "scipy",
    "expression": expression,
    "normalized_input": parsed.normalized,
    "symbol": symbol,
    "method": method if bracket is not None else "secant",
    "root": float(result.root),
    "iterations": result.iterations,
    "function_calls": result.function_calls,
    "converged": result.converged,
  }


def optimize_scalar_expression(
  expression: str,
  symbol: str,
  bounds: list[float] | None = None,
  goal: str = "minimize",
  method: str | None = None,
) -> dict[str, Any]:
  parsed = parse_expression(expression)
  sym = Symbol(symbol)
  fn = lambdify(sym, parsed.expr, modules=["numpy"])

  objective = fn
  if goal == "maximize":
    objective = lambda x: -fn(x)

  use_method = method
  kwargs: dict[str, Any] = {}
  if bounds is not None:
    if len(bounds) != 2:
      raise ValueError("bounds must contain exactly two numeric values")
    kwargs["bounds"] = tuple(bounds)
    use_method = use_method or "bounded"

  result = minimize_scalar(objective, method=use_method, **kwargs)
  if not result.success:
    raise RuntimeError(f"scalar optimization failed: {result.message}")

  optimum_value = float(fn(result.x))
  if goal == "maximize":
    optimum_value = float(fn(result.x))

  return {
    "backend": "scipy",
    "expression": expression,
    "normalized_input": parsed.normalized,
    "symbol": symbol,
    "goal": goal,
    "method": use_method or "brent",
    "x": float(result.x),
    "value": optimum_value,
    "iterations": getattr(result, "nit", None),
    "function_calls": result.nfev,
    "success": bool(result.success),
  }

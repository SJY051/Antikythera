from __future__ import annotations

from typing import Any, Literal

from mcp.server.fastmcp import FastMCP

from .backends.qalculate import qalculate_compute
from .backends.scientific import numeric_solve, optimize_scalar_expression
from .core import (
  differentiate_expression,
  evaluate_expression,
  integrate_expression,
  matrix_compute,
  numeric_compute,
  solve_equation,
  unit_convert,
)
from .errors import format_tool_error
from .runtime import backend_status
from .timed import run_with_timeout

mcp = FastMCP("Antikythera", json_response=True)


def _safe_call(func: Any, *args: Any, **kwargs: Any) -> dict[str, Any]:
  try:
    return func(*args, **kwargs)
  except TimeoutError:
    raise
  except Exception as exc:
    raise RuntimeError(format_tool_error(exc.__class__.__name__, str(exc))) from exc


@mcp.tool()
def evaluate_expression_tool(
  expression: str,
  substitutions: dict[str, Any] | None = None,
  numeric: bool = False,
  precision: int = 50,
) -> dict[str, Any]:
  """Evaluate and optionally numerically approximate a symbolic expression."""
  return _safe_call(
    evaluate_expression,
    expression,
    substitutions,
    numeric=numeric,
    precision=precision,
  )


@mcp.tool()
def solve_equation_tool(
  equation: str,
  symbol: str,
  substitutions: dict[str, Any] | None = None,
  timeout_ms: int = 10000,
) -> dict[str, Any]:
  """Solve an equation for a target symbol."""
  return _safe_call(
    solve_equation,
    equation,
    symbol,
    substitutions,
  )


@mcp.tool()
def differentiate_tool(
  expression: str,
  symbol: str,
  order: int = 1,
) -> dict[str, Any]:
  """Differentiate an expression with respect to a symbol."""
  return _safe_call(
    differentiate_expression,
    expression,
    symbol,
    order=order,
  )


@mcp.tool()
def integrate_tool(
  expression: str,
  symbol: str,
  lower_bound: str | None = None,
  upper_bound: str | None = None,
  timeout_ms: int = 10000,
) -> dict[str, Any]:
  """Integrate an expression indefinitely or between explicit bounds."""
  return _safe_call(
    integrate_expression,
    expression,
    symbol,
    lower_bound=lower_bound,
    upper_bound=upper_bound,
  )


@mcp.tool()
def matrix_compute_tool(
  operation: Literal["determinant", "inverse", "transpose", "eigenvalues", "add", "multiply"],
  matrix: list[list[float]],
  other_matrix: list[list[float]] | None = None,
) -> dict[str, Any]:
  """Run a matrix operation on one or two matrices."""
  return _safe_call(
    matrix_compute,
    operation,
    matrix,
    other_matrix,
  )


@mcp.tool()
def unit_convert_tool(
  value: float,
  from_unit: str,
  to_unit: str,
) -> dict[str, Any]:
  """Convert a quantity from one unit to another."""
  return _safe_call(unit_convert, value, from_unit, to_unit)


@mcp.tool()
def numeric_compute_tool(
  expression: str,
  variable: str,
  start: float,
  end: float,
  samples: int = 100,
) -> dict[str, Any]:
  """Sample a numeric expression over an interval and summarize the range."""
  return _safe_call(numeric_compute, expression, variable, start, end, samples=samples)


@mcp.tool()
def qalculate_compute_tool(
  expression: str,
  timeout_ms: int = 3000,
  terse: bool = True,
) -> dict[str, Any]:
  """Evaluate a utility-style calculation through the optional Qalculate backend."""
  return qalculate_compute(expression, timeout_ms=timeout_ms, terse=terse)


@mcp.tool()
def backend_status_tool() -> dict[str, Any]:
  """Report which core and optional Antikythera backends are currently available."""
  return backend_status()


@mcp.tool()
def numeric_solve_tool(
  expression: str,
  symbol: str,
  bracket: list[float] | None = None,
  initial_guess: float | None = None,
  method: str = "brentq",
) -> dict[str, Any]:
  """Find a numeric root for an expression through the optional SciPy backend."""
  return _safe_call(
    numeric_solve,
    expression,
    symbol,
    bracket=bracket,
    initial_guess=initial_guess,
    method=method,
  )


@mcp.tool()
def optimize_scalar_tool(
  expression: str,
  symbol: str,
  bounds: list[float] | None = None,
  goal: Literal["minimize", "maximize"] = "minimize",
  method: str | None = None,
) -> dict[str, Any]:
  """Optimize a scalar expression through the optional SciPy backend."""
  return _safe_call(
    optimize_scalar_expression,
    expression,
    symbol,
    bounds=bounds,
    goal=goal,
    method=method,
  )


def main() -> None:
  mcp.run(transport="stdio")

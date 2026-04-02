from __future__ import annotations

import re
from dataclasses import dataclass

from sympy import Eq
from sympy.core.expr import Expr
from sympy.parsing.sympy_parser import (
  convert_xor,
  function_exponentiation,
  implicit_multiplication_application,
  parse_expr,
  standard_transformations,
)

TRANSFORMATIONS = (
  standard_transformations
  + (
    convert_xor,
    implicit_multiplication_application,
    function_exponentiation,
  )
)

UNICODE_REPLACEMENTS = {
  "−": "-",
  "–": "-",
  "—": "-",
  "×": "*",
  "·": "*",
  "÷": "/",
  "π": "pi",
}


@dataclass(frozen=True)
class ParsedExpression:
  original: str
  normalized: str
  expr: Expr


@dataclass(frozen=True)
class ParsedEquation:
  original: str
  normalized: str
  equation: Eq


def normalize_expression_text(expression: str) -> str:
  if not isinstance(expression, str) or not expression.strip():
    raise ValueError("expression must be a non-empty string")

  normalized = expression.strip()
  for src, dst in UNICODE_REPLACEMENTS.items():
    normalized = normalized.replace(src, dst)

  normalized = re.sub(r"\s+", " ", normalized)
  return normalized


def parse_expression(expression: str) -> ParsedExpression:
  normalized = normalize_expression_text(expression)
  expr = parse_expr(normalized, transformations=TRANSFORMATIONS, evaluate=True)
  return ParsedExpression(
    original=expression,
    normalized=normalized,
    expr=expr,
  )


def parse_equation(equation: str) -> ParsedEquation:
  normalized = normalize_expression_text(equation)

  if "=" in normalized:
    left, right = normalized.split("=", 1)
    parsed = Eq(
      parse_expr(left.strip(), transformations=TRANSFORMATIONS, evaluate=True),
      parse_expr(right.strip(), transformations=TRANSFORMATIONS, evaluate=True),
    )
  else:
    parsed = Eq(parse_expr(normalized, transformations=TRANSFORMATIONS, evaluate=True), 0)

  return ParsedEquation(
    original=equation,
    normalized=normalized,
    equation=parsed,
  )

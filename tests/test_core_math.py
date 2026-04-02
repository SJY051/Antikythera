from __future__ import annotations

import unittest

from antikythera.backends.qalculate import find_qalc, qalculate_compute
from antikythera.backends.scientific import numeric_solve, optimize_scalar_expression
from antikythera.core import (
  differentiate_expression,
  evaluate_expression,
  integrate_expression,
  matrix_compute,
  solve_equation,
  unit_convert,
)
from antikythera.parsing import parse_equation, parse_expression
from antikythera.runtime import backend_status
from antikythera.timed import run_with_timeout


class CoreMathTests(unittest.TestCase):
  def test_evaluate_expression_symbolic(self) -> None:
    result = evaluate_expression("x**2 + 2*x + 1")
    self.assertEqual(result["backend"], "sympy")
    self.assertEqual(result["symbolic"], "x**2 + 2*x + 1")

  def test_solve_equation(self) -> None:
    result = solve_equation("x**2 - 4 = 0", "x")
    self.assertEqual(result["backend"], "sympy")
    self.assertEqual(result["solutions"], ["-2", "2"])

  def test_differentiate_expression(self) -> None:
    result = differentiate_expression("x**3", "x")
    self.assertEqual(result["result"], "3*x**2")

  def test_integrate_expression(self) -> None:
    result = integrate_expression("x", "x", lower_bound="0", upper_bound="2")
    self.assertEqual(result["mode"], "definite")
    self.assertEqual(result["result"], "2")

  def test_matrix_compute(self) -> None:
    result = matrix_compute("determinant", [[1, 2], [3, 4]])
    self.assertEqual(result["result"], "-2")

  def test_unit_convert(self) -> None:
    result = unit_convert(1, "meter", "centimeter")
    self.assertEqual(result["backend"], "pint")
    self.assertAlmostEqual(result["magnitude"], 100.0)

  @unittest.skipIf(find_qalc() is None, "Qalculate is not installed")
  def test_qalculate_compute(self) -> None:
    result = qalculate_compute("5 m to ft")
    self.assertEqual(result["backend"], "qalculate")
    self.assertEqual(result["exit_code"], 0)
    self.assertIn("ft", str(result["result"]))

  def test_parser_normalizes_xor_and_implicit_multiplication(self) -> None:
    parsed = parse_expression("2x^2")
    self.assertEqual(parsed.normalized, "2x^2")
    self.assertEqual(str(parsed.expr), "2*x**2")

  def test_parser_normalizes_equation_text(self) -> None:
    parsed = parse_equation("2x + 3 = 0")
    self.assertEqual(parsed.normalized, "2x + 3 = 0")
    self.assertEqual(str(parsed.equation), "Eq(2*x + 3, 0)")

  def test_backend_status_reports_optional_policy(self) -> None:
    status = backend_status()
    self.assertEqual(status["server"], "Antikythera")
    self.assertFalse(status["policy"]["core_tools_require_optional_backends"])
    self.assertTrue(status["policy"]["optional_backends_are_explicit_only"])
    self.assertIn("sympy", status["core"])
    self.assertIn("qalculate", status["optional"])

  def test_numeric_solve(self) -> None:
    result = numeric_solve("x^2 - 2", "x", bracket=[1.0, 2.0])
    self.assertEqual(result["backend"], "scipy")
    self.assertTrue(result["converged"])
    self.assertAlmostEqual(result["root"], 2 ** 0.5, places=8)

  def test_optimize_scalar_expression(self) -> None:
    result = optimize_scalar_expression("(x - 3)^2 + 1", "x", bounds=[0.0, 10.0], goal="minimize")
    self.assertEqual(result["backend"], "scipy")
    self.assertTrue(result["success"])
    self.assertAlmostEqual(result["x"], 3.0, places=6)
    self.assertAlmostEqual(result["value"], 1.0, places=6)

  def test_run_with_timeout_returns_successful_result(self) -> None:
    result = run_with_timeout(evaluate_expression, "2x^2 + 1", timeout_ms=2000)
    self.assertEqual(result["symbolic"], "2*x**2 + 1")

  def test_run_with_timeout_raises_on_timeout(self) -> None:
    with self.assertRaises(TimeoutError):
      run_with_timeout(integrate_expression, "x", "x", timeout_ms=1)

  def test_run_with_timeout_formats_parse_errors(self) -> None:
    with self.assertRaisesRegex(RuntimeError, "parse_error"):
      run_with_timeout(evaluate_expression, "solve 2x+3=0 for x", timeout_ms=2000)


if __name__ == "__main__":
  unittest.main()

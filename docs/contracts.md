# Antikythera Contracts

## Core positioning

Antikythera is a narrow, deterministic math companion for MCP agents.

It should stay:

- small enough for an agent to choose tools predictably
- structured enough to avoid free-form code execution for common math work
- strict about optional backends staying optional

## Tool contracts

### evaluate_expression

- backend: `sympy`
- role: symbolic evaluation and optional numeric approximation
- returns:
  - `backend`
  - `expression`
  - `normalized_input`
  - `symbolic`
  - `numeric` when requested

### solve_equation

- backend: `sympy`
- role: solve one algebraic equation for one target symbol
- v0.1 scope:
  - one equation
  - one variable target
  - symbolic solve first
- explicitly not in scope yet:
  - inequalities
  - ODE/PDE solving
  - multi-equation system solving

### differentiate

- backend: `sympy`
- role: symbolic derivative by variable and order

### integrate

- backend: `sympy`
- role: symbolic definite or indefinite integration
- note:
  - pathological expressions may still require a future hard timeout layer

### matrix_compute

- backend: `sympy`
- role: exact matrix operations on structured matrix inputs

### unit_convert

- backend: `pint`
- role: deterministic unit conversion
- note:
  - this is expected to be one of the most practically valuable tools

### numeric_compute

- backend: `numpy`
- role: sample an expression over an interval and summarize the numeric range

### qalculate_compute

- backend: `qalculate`
- role: optional utility calculation adapter
- contract:
  - must never be called implicitly by core tools
  - failure to find or run Qalculate must not break the rest of Antikythera

### backend_status

- role: expose which core and optional backends are actually available at runtime
- purpose:
  - make optional dependency boundaries visible
  - help agents avoid assuming SciPy, Qalculate, DuckDB, or future adapters are present

### numeric_solve

- backend: `scipy`
- role: numeric root finding for expressions that are better handled numerically than symbolically
- contract:
  - explicit optional scientific extension
  - requires either a `bracket` or an `initial_guess`

### optimize_scalar

- backend: `scipy`
- role: numeric scalar minimization or maximization
- contract:
  - explicit optional scientific extension
  - bounded optimization is preferred when the caller can provide bounds

## Parsing policy

Parsing should normalize limited, common syntax differences without pretending to understand arbitrary prose.

Supported normalization targets currently include:

- `^`
- implicit multiplication
- function exponentiation
- common Unicode operators

Future parsing work should improve normalization and error messages, not widen the scope into unconstrained natural-language math.

## Error shape goals

Preferred top-level categories:

- `parse_error`
- `unsupported_syntax`
- `domain_error`
- `dimension_mismatch`
- `timeout`
- `optional_backend_unavailable`

These are design targets for future structured errors.

Current implementation already aims to surface agent-correctable messages for common parse and unit failures rather than raw low-level tracebacks.

## Timeout policy

Timeout protection is still an open hardening area.

- core math functions stay deterministic and importable for local tests
- optional utility backends can keep backend-specific timeout controls
- strong timeout isolation for symbolic heavy cases is a future improvement, not a solved promise of v0.1

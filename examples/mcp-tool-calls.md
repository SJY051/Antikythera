# Antikythera Example Tool Calls

These examples show the intended shape of Antikythera calls from an MCP-aware agent.

## Evaluate an expression

Input:

```json
{
  "expression": "2x^2 + 1",
  "numeric": false,
  "precision": 30
}
```

Expected result shape:

```json
{
  "backend": "sympy",
  "expression": "2x^2 + 1",
  "normalized_input": "2x^2 + 1",
  "symbolic": "2*x**2 + 1"
}
```

## Solve an equation

Input:

```json
{
  "equation": "x^2 - 4 = 0",
  "symbol": "x"
}
```

Expected result shape:

```json
{
  "backend": "sympy",
  "equation": "Eq(x**2 - 4, 0)",
  "normalized_input": "x^2 - 4 = 0",
  "symbol": "x",
  "solutions": ["-2", "2"]
}
```

## Definite integral

Input:

```json
{
  "expression": "x",
  "symbol": "x",
  "lower_bound": "0",
  "upper_bound": "2"
}
```

Expected result shape:

```json
{
  "backend": "sympy",
  "expression": "x",
  "normalized_input": "x",
  "symbol": "x",
  "mode": "definite",
  "normalized_lower_bound": "0",
  "normalized_upper_bound": "2",
  "result": "2"
}
```

## Unit conversion

Input:

```json
{
  "value": 5,
  "from_unit": "meter",
  "to_unit": "foot"
}
```

Expected result shape:

```json
{
  "backend": "pint",
  "input": "5.0 meter",
  "output": "16.404199475065617 foot",
  "magnitude": 16.404199475065617,
  "unit": "foot"
}
```

## Optional Qalculate utility call

Input:

```json
{
  "expression": "5 m to ft",
  "terse": true,
  "timeout_ms": 3000
}
```

## Numeric root finding

Input:

```json
{
  "expression": "x^2 - 2",
  "symbol": "x",
  "bracket": [1.0, 2.0]
}
```

Expected result shape:

```json
{
  "backend": "scipy",
  "expression": "x^2 - 2",
  "symbol": "x",
  "root": 1.4142135623730951,
  "converged": true
}
```

## Scalar optimization

Input:

```json
{
  "expression": "(x - 3)^2 + 1",
  "symbol": "x",
  "bounds": [0.0, 10.0],
  "goal": "minimize"
}
```

Expected result shape:

```json
{
  "backend": "scipy",
  "expression": "(x - 3)^2 + 1",
  "symbol": "x",
  "goal": "minimize",
  "x": 3.0,
  "value": 1.0,
  "success": true
}
```

Expected result shape:

```json
{
  "expression": "5 m to ft",
  "backend": "qalculate",
  "ok": "true",
  "result": "16 ft + 4.850393701 in"
}
```

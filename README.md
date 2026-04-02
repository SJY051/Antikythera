# Antikythera

Antikythera is a Python-first local math MCP server intended as a practical, low-cost alternative to a Wolfram-style helper for AI agents.

The first version focuses on a reliable core:

- symbolic expression evaluation
- equation solving
- differentiation
- integration
- matrix operations
- unit conversion
- optional utility calculations through Qalculate

The first scientific extension layer now also supports:

- numeric root finding through SciPy
- scalar minimization and maximization through SciPy

## Target scenarios

Antikythera is meant for MCP-first agent environments that need dependable calculation help without depending on a broad free-form code execution loop.

Examples:

- agents that can call tools but should not spend tokens writing ad hoc Python for every calculation
- environments such as Claude Desktop where a math-specific MCP surface is more practical than a notebook workflow
- local automation flows that need deterministic math, symbolic manipulation, and unit conversion

## Non-goals for v0.1

Antikythera is not trying to be:

- a full Wolfram replacement
- a notebook environment
- a general SQL or dataframe workbench
- a natural-language math tutor that accepts arbitrary prose prompts

The design leaves room for backend expansion later:

- `core`: SymPy, NumPy, mpmath, Pint
- `scientific`: SciPy-backed numerical routines
- `utility`: lightweight adapters such as Qalculate
- `heavy`: optional SageMath or other external engines

## Why this shape

Instead of chasing a single paid service, Antikythera keeps the calculation engine local and cheap, while remaining extensible enough to grow into a broader reasoning tool later.

## What feels ready today

Antikythera already works well for:

- symbolic expressions that benefit from normalization before evaluation
- simple algebraic equation solving
- definite and indefinite integrals
- structured matrix operations
- deterministic unit conversion
- quick utility calculations through an optional Qalculate adapter

## Current tool surface

- `evaluate_expression`
- `solve_equation`
- `differentiate`
- `integrate`
- `matrix_compute`
- `unit_convert`
- `qalculate_compute`
- `backend_status`
- `numeric_solve`
- `optimize_scalar`

## Parsing and normalization

The most fragile part of this project is not the math backend but the input surface. Antikythera therefore separates parsing from execution and normalizes expressions before evaluation.

Current normalization covers:

- `^` exponent syntax
- implicit multiplication such as `2x`
- function exponentiation such as `sin^2(x)`
- common Unicode operator characters

Symbolic and numeric tools return `normalized_input` so agents can inspect what was actually executed.

## Timeout safety

Timeout handling remains a future hardening area.

- the current MCP surface prefers reliable direct execution over a brittle timeout wrapper
- optional utility backends such as Qalculate keep their own timeout controls
- stronger process isolation for expensive symbolic work is planned, but not claimed as fully solved in v0.1

## Optional backend contract

Optional layers such as Qalculate, SciPy, SageMath, or Mathics must never become hidden requirements for the core tools.

- core tools must work with Python-only dependencies
- optional backends must live in separate backend modules or separate tool paths
- results should report the backend used
- optional backend failure must degrade gracefully instead of breaking core behavior

## Project layout

- `src/antikythera/server.py`: MCP server entrypoint
- `src/antikythera/core.py`: core symbolic and numeric operations
- `src/antikythera/parsing.py`: expression parsing helpers
- `src/antikythera/backends/`: future backend adapters
- `docs/architecture.md`: extension and layering plan
- `docs/contracts.md`: tool contracts, parsing policy, and non-goals
- `docs/quickstart.md`: install, attach, and first-call guide
- `docs/roadmap.md`: near-term direction and extension priorities
- `examples/mcp-tool-calls.md`: concrete tool-call examples
- `examples/agent-usage-notes.md`: practical caller guidance
- `CHANGELOG.md`: release notes

## Run locally

```powershell
pip install -e .
python -m antikythera
```

The server runs over stdio and is intended to be attached as an MCP tool server.

## Verify quickly

After attachment, these calls are a good first smoke test:

- `evaluate_expression("2x^2 + 1")`
- `solve_equation("x^2 - 4 = 0", "x")`
- `unit_convert(5, "meter", "foot")`
- `backend_status()`

## Codex MCP attachment

Add this to the Codex config:

```toml
[mcp_servers.antikythera]
command = "python"
args = ["-m", "antikythera"]
```

## Status

This project is currently in an early public-ready alpha shape:

- core math tools are working
- optional backend boundaries are explicit
- parsing normalization is present but still an active improvement area
- timeout isolation for heavy symbolic workloads is intentionally deferred to a future hardening pass

## Related docs

- [Quickstart](docs/quickstart.md)
- [Architecture](docs/architecture.md)
- [Contracts](docs/contracts.md)
- [Roadmap](docs/roadmap.md)
- [Example Tool Calls](examples/mcp-tool-calls.md)
- [Agent Usage Notes](examples/agent-usage-notes.md)
- [Contributing](CONTRIBUTING.md)

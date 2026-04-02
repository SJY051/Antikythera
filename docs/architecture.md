# Antikythera Architecture

## Goal

Build a local math-and-structure MCP server that begins as a dependable symbolic/numeric calculator and can later expand into a richer computational workbench.

## Product position

Antikythera is not trying to replace Wolfram in full.

Its intended niche is narrower:

- a local math companion for MCP-first agents
- a deterministic alternative to repeated ad hoc code-writing loops
- a structured calculation surface for environments where full notebook execution is not the right fit

## Layering

### Layer 1: Core symbolic and unit operations

Always-on local Python dependencies:

- SymPy
- NumPy
- mpmath
- Pint

These power the first stable tools:

- expression evaluation
- equation solving
- calculus
- matrices
- unit conversion

### Layer 2: Scientific extensions

Optional dependencies:

- SciPy

These enable later additions such as:

- optimization
- interpolation
- statistical routines
- signal processing

The first scientific extension tools are intentionally narrow:

- numeric root finding
- scalar optimization

### Layer 3: External or heavy adapters

Optional runtime adapters:

- Qalculate CLI
- SageMath
- Mathics3

These should remain isolated behind backend modules so the core tool surface does not become unstable.

Qalculate is the first intended adapter in this layer because it is light, practical, and complements the symbolic core with fast utility math, constants, and unit-heavy queries.

## Design principles

1. Keep the first version small and dependable.
2. Prefer deterministic local execution over opaque remote services.
3. Separate parsing from execution.
4. Expose a calm MCP surface with clear argument contracts.
5. Add heavier engines only as backend adapters, not as core assumptions.
6. Keep optional adapters from leaking into core execution paths.
7. Prefer narrower dependable tools over a fuzzy pseudo-CAS.

## Initial roadmap

1. Stand up the stdio MCP server with six core tools.
2. Verify symbolic, numeric, matrix, and unit workflows locally.
3. Add optional SciPy-backed numerical tools when needed.
4. Consider a Qalculate adapter for fast utility math.
5. Consider SageMath only if the workload genuinely asks for it.

## Immediate risks

1. Parsing normalization is likely the hardest practical part of the project.
2. Expensive symbolic operations will need timeout guards soon.
3. Tool contracts must stay narrow enough for agents to choose them predictably.

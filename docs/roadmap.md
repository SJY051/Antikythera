# Antikythera Roadmap

## Current shape

Antikythera is already in a useful alpha state:

- core symbolic math
- matrix operations
- unit conversion
- parsing normalization
- optional Qalculate adapter
- optional SciPy scientific layer

## Near-term priorities

1. Better structured errors
2. Safer timeout hardening for expensive symbolic cases
3. More parsing normalization for messy agent inputs
4. A few carefully chosen scientific tools beyond root finding and scalar optimization

## Candidate extensions

- interpolation
- lightweight statistics helpers
- bounded numeric integration
- richer matrix modes
- optional Mathics or Sage adapters, only if real demand appears

## Things to avoid

- pretending to be a full Wolfram replacement too early
- letting optional backends become hidden requirements
- expanding into a general data workbench before the math core is mature

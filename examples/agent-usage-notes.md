# Agent Usage Notes

## What works best

Antikythera works best when the caller already knows the category of the operation:

- evaluate
- solve
- differentiate
- integrate
- matrix
- unit conversion

It is not meant to accept arbitrary conversational math requests as free-form prose.

## Good inputs

- `2x^2 + 1`
- `x^2 - 4 = 0`
- `sin(pi/4)`
- `5 meter -> foot` expressed through structured fields for unit conversion

## Bad inputs

- `solve this please`
- `what is the answer to this math thing`
- `do the whole derivation for me`

## Correction loop

If Antikythera returns a `parse_error`, the agent should retry with:

- explicit multiplication, such as `2*x`
- exponent syntax like `x**2`
- less prose and more direct math notation

# Contributing

Thanks for taking an interest in Antikythera.

## Current priorities

The most valuable improvements right now are:

- better parsing normalization
- clearer structured errors
- stronger tool contracts and schema clarity
- safer timeout hardening for expensive symbolic operations

## Development workflow

```powershell
pip install -e .
python -m unittest discover -s tests -t .
```

## Ground rules

- keep core tools independent from optional backends
- prefer narrow, predictable APIs over broad magic behavior
- document scope changes in `docs/contracts.md`
- add tests when parsing or tool behavior changes

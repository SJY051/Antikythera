# Antikythera Quickstart

## Install

```powershell
pip install -e .
```

Optional Qalculate support on Windows:

```powershell
winget install --id Qalculate.Qalculate --accept-package-agreements --accept-source-agreements --disable-interactivity
```

## Run directly

```powershell
python -m antikythera
```

## Attach to Codex

Add this to `C:\Users\User\.codex\config.toml`:

```toml
[mcp_servers.antikythera]
command = "python"
args = ["-m", "antikythera"]
```

Then restart Codex.

## First smoke tests

Call:

- `evaluate_expression` with `2x^2 + 1`
- `solve_equation` with `x^2 - 4 = 0`
- `unit_convert` with `5 meter -> foot`
- `backend_status`

## Expectations

Antikythera is strongest when:

- the input is mathematical rather than conversational prose
- the caller prefers structured tools over ad hoc Python code generation
- exact symbolic work or deterministic unit conversion matters

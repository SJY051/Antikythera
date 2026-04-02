from __future__ import annotations

from importlib import metadata

from .backends.qalculate import find_qalc


def _package_version(name: str) -> str | None:
  try:
    return metadata.version(name)
  except metadata.PackageNotFoundError:
    return None


def backend_status() -> dict[str, object]:
  qalc_path = find_qalc()

  return {
    "server": "Antikythera",
    "core": {
      "sympy": _package_version("sympy"),
      "numpy": _package_version("numpy"),
      "mpmath": _package_version("mpmath"),
      "pint": _package_version("pint"),
      "mcp": _package_version("mcp"),
    },
    "optional": {
      "scipy": {
        "available": _package_version("scipy") is not None,
        "version": _package_version("scipy"),
      },
      "qalculate": {
        "available": qalc_path is not None,
        "binary": qalc_path,
      },
      "duckdb": {
        "available": _package_version("duckdb") is not None,
        "version": _package_version("duckdb"),
      },
      "mathics3": {
        "available": _package_version("Mathics3") is not None,
        "version": _package_version("Mathics3"),
      },
    },
    "policy": {
      "core_tools_require_optional_backends": False,
      "optional_backends_are_explicit_only": True,
    },
  }

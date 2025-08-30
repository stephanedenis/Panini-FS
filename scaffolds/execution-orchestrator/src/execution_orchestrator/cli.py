from __future__ import annotations
import sys
import typer

try:
    from .drivers import get as get_driver
except Exception:
    # allow CLI in scaffold without drivers present
    def get_driver(name: str):  # type: ignore
        return None

app = typer.Typer(help="Execution Orchestrator CLI")

@app.command()
def version():
    """Print version."""
    print("execution-orchestrator 0.1.0")

@app.command()
def run(mission: str, backend: str = typer.Option("local", help="local|colab|cloud")):
    """Run a mission on a backend (stub)."""
    drv = get_driver(backend)
    if not drv:
        print(f"Unknown backend: {backend}", file=sys.stderr)
        raise typer.Exit(code=2)
    code = drv.run(mission)
    raise typer.Exit(code=code)

if __name__ == "__main__":
    app()

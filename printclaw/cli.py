import json

import typer
import uvicorn

from printclaw import __version__
from printclaw.core.agent import PrintclawAgent
from printclaw.core.context import AgentContext

app = typer.Typer(help="Printclaw printer diagnostics CLI")
sessions_app = typer.Typer(help="Session history commands")
kb_app = typer.Typer(help="Knowledgebase commands")
app.add_typer(sessions_app, name="sessions")
app.add_typer(kb_app, name="kb")

agent = PrintclawAgent()


@app.command()
def version() -> None:
    typer.echo(__version__)


@app.command()
def web(host: str = "127.0.0.1", port: int = 8080) -> None:
    uvicorn.run("printclaw.web.app:app", host=host, port=port, reload=False)


@app.command()
def scan(target_ip: str = "127.0.0.1") -> None:
    ctx = AgentContext(target_ip=target_ip)
    result = agent.run_diagnostics(ctx)
    typer.echo(json.dumps({"session_id": result["session_id"], "issues": result["issues_found"]}, indent=2))


@app.command()
def diagnose(export: str = typer.Option("json", "--export", help="json|txt|md"), target_ip: str = "127.0.0.1") -> None:
    payload = agent.run_diagnostics(AgentContext(target_ip=target_ip))
    out = agent.report_builder.export(payload, export)
    payload["export_paths"][export] = str(out)
    agent.session_store.save(payload["session_id"], payload)
    typer.echo(f"Session {payload['session_id']} complete. Exported: {out}")


@sessions_app.command("list")
def sessions_list() -> None:
    typer.echo(json.dumps(agent.session_store.list_sessions(), indent=2))


@sessions_app.command("show")
def sessions_show(session_id: str) -> None:
    payload = agent.session_store.get(session_id)
    if not payload:
        raise typer.BadParameter("Session not found")
    typer.echo(json.dumps(payload, indent=2))


@sessions_app.command("export")
def sessions_export(session_id: str, format: str = typer.Option("json", "--format")) -> None:
    payload = agent.session_store.get(session_id)
    if not payload:
        raise typer.BadParameter("Session not found")
    out = agent.report_builder.export(payload, format)
    typer.echo(str(out))


@kb_app.command("search")
def kb_search(query: str) -> None:
    typer.echo(json.dumps(agent.kb_loader.search(query), indent=2))

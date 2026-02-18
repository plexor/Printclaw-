from fastapi import APIRouter, HTTPException, Query, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

from printclaw.core.agent import PrintclawAgent
from printclaw.core.context import AgentContext

router = APIRouter()
templates = Jinja2Templates(directory="printclaw/web/templates")
agent = PrintclawAgent()


@router.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/sessions", response_class=HTMLResponse)
def sessions_page(request: Request):
    return templates.TemplateResponse("sessions.html", {"request": request})


@router.get("/sessions/{session_id}", response_class=HTMLResponse)
def session_page(request: Request, session_id: str):
    return templates.TemplateResponse("session.html", {"request": request, "session_id": session_id})


@router.get("/api/status")
def status():
    return {"status": "ok", "app": "printclaw", "safe_mode": True}


@router.get("/api/skills")
def skills():
    return {"skills": agent.registry.list()}


@router.post("/api/diagnose")
def diagnose(target_ip: str | None = None):
    ctx = AgentContext(target_ip=target_ip)
    return agent.run_diagnostics(ctx)


@router.get("/api/sessions")
def list_sessions():
    return {"sessions": agent.session_store.list_sessions()}


@router.get("/api/sessions/{session_id}")
def get_session(session_id: str):
    payload = agent.session_store.get(session_id)
    if not payload:
        raise HTTPException(status_code=404, detail="Session not found")
    return payload


@router.delete("/api/sessions/{session_id}")
def delete_session(session_id: str):
    return {"deleted": agent.session_store.delete(session_id)}


@router.get("/api/sessions/{session_id}/export")
def export_session(session_id: str, format: str = Query("json", pattern="^(json|txt|md)$")):
    payload = agent.session_store.get(session_id)
    if not payload:
        raise HTTPException(status_code=404, detail="Session not found")
    path = agent.report_builder.export(payload, format)
    payload["export_paths"][format] = str(path)
    agent.session_store.save(session_id, payload)
    return FileResponse(path)


@router.get("/api/kb/search")
def kb_search(q: str = Query(..., min_length=1)):
    return {"matches": agent.kb_loader.search(q)}


@router.get("/api/logs/latest")
def latest_logs():
    return {"entries": ["startup ok", "registry loaded", "ready"]}

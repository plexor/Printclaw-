from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from printclaw.web.routes import router

app = FastAPI(title="Printclaw")
app.mount("/static", StaticFiles(directory="printclaw/web/static"), name="static")
app.include_router(router)

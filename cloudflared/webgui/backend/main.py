"""Cloudflared Web GUI — FastAPI application entry point.

Served exclusively through Home Assistant Ingress (no host port is
published). Authentication is therefore handled by Home Assistant itself;
as defense in depth, requests are only accepted from the Supervisor's
ingress gateway (172.30.32.2) unless WEBGUI_DEV=1 is set.
"""
from __future__ import annotations

import os
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from .instances import logwatcher, supervisor
from .routers import health, logs, options, wizard

INGRESS_GATEWAY = "172.30.32.2"
DEV_MODE = os.environ.get("WEBGUI_DEV", "") == "1"
STATIC_DIR = Path(os.environ.get("WEBGUI_STATIC", "/opt/webgui/static"))


@asynccontextmanager
async def lifespan(app: FastAPI):
    await logwatcher.start()
    yield
    await logwatcher.stop()
    await supervisor.close()


app = FastAPI(title="Cloudflared Web GUI", lifespan=lifespan)


@app.middleware("http")
async def ingress_only(request: Request, call_next):
    if not DEV_MODE:
        client = request.client.host if request.client else ""
        if client not in (INGRESS_GATEWAY, "127.0.0.1", "::1"):
            return JSONResponse(
                {"detail": "Access is only allowed through Home Assistant Ingress"},
                status_code=403,
            )
    return await call_next(request)


app.include_router(health.router)
app.include_router(options.router)
app.include_router(logs.router)
app.include_router(wizard.router)

# Mounted last so /api/* keeps precedence. All frontend assets use relative
# paths (vite base './' + hash routing) so the app works under the dynamic
# ingress path prefix without any base-path configuration.
if STATIC_DIR.is_dir():
    app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")

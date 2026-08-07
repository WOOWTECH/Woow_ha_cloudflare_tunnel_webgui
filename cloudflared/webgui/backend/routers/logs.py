"""Log endpoints — snapshot + live WebSocket stream.

The content is the add-on's own log as served by the Supervisor, i.e. exactly
what the HA add-on Log tab shows (bashio + cloudflared lines), minus ANSI
color codes.
"""
import asyncio
import os

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from ..instances import logwatcher

router = APIRouter(prefix="/api/logs", tags=["logs"])

INGRESS_GATEWAY = "172.30.32.2"
DEV_MODE = os.environ.get("WEBGUI_DEV", "") == "1"


@router.get("")
async def get_logs() -> dict:
    return {
        "lines": logwatcher.snapshot(),
        "follow_supported": logwatcher.follow_supported,
    }


@router.websocket("/stream")
async def stream_logs(ws: WebSocket) -> None:
    # HTTP middleware does not cover WebSockets — enforce the ingress-only
    # guard here as well.
    client = ws.client.host if ws.client else ""
    if not DEV_MODE and client not in (INGRESS_GATEWAY, "127.0.0.1", "::1"):
        await ws.close(code=4403)
        return
    await ws.accept()
    for line in logwatcher.snapshot():
        await ws.send_text(line)
    queue = logwatcher.subscribe()
    try:
        while True:
            line = await queue.get()
            await ws.send_text(line)
    except (WebSocketDisconnect, asyncio.CancelledError):
        pass
    finally:
        logwatcher.unsubscribe(queue)

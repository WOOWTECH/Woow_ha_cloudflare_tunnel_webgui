"""Read/write the add-on's Supervisor options — the single source of truth.

PUT semantics for ``tunnel_token``:
- field omitted or ``null``  → keep the currently stored token (if any)
- empty string ``""``        → remove the token (switch to local-managed mode)
- non-empty string           → store the new token (remote-managed mode)
"""
from fastapi import APIRouter, HTTPException, Query

from ..instances import supervisor
from ..models import AddonOptions, OptionsRead
from ..supervisor import SupervisorError

router = APIRouter(prefix="/api", tags=["options"])


@router.get("/options", response_model=OptionsRead)
async def get_options() -> OptionsRead:
    try:
        options = await supervisor.get_options()
    except SupervisorError as exc:
        raise HTTPException(exc.status, str(exc)) from exc
    return OptionsRead.from_supervisor(options)


@router.put("/options")
async def put_options(
    body: AddonOptions,
    restart: bool = Query(
        default=False,
        description="Restart the add-on after saving so the options take "
        "effect (identical to pressing SAVE + RESTART on the HA "
        "configuration page).",
    ),
) -> dict:
    try:
        current = await supervisor.get_options()
    except SupervisorError as exc:
        raise HTTPException(exc.status, str(exc)) from exc

    options = body.to_supervisor_options()

    # Token keep/remove/replace semantics (see module docstring).
    if body.tunnel_token is None:
        existing = (current.get("tunnel_token") or "").strip()
        if existing:
            options["tunnel_token"] = existing

    try:
        await supervisor.validate_options(options)
        await supervisor.set_options(options)
    except SupervisorError as exc:
        raise HTTPException(exc.status, str(exc)) from exc

    restarting = False
    if restart:
        restarting = True
        await supervisor.restart_self()

    return {"result": "ok", "restarting": restarting}


@router.post("/restart")
async def restart_addon() -> dict:
    """Restart the whole add-on (prepare re-runs, config re-applies)."""
    await supervisor.restart_self()
    return {"result": "ok", "restarting": True}

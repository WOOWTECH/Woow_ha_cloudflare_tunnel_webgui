# Cloudflared Web GUI — Home Assistant Add-on

[繁體中文](README_zh-TW.md)

**A fork of [homeassistant-apps/app-cloudflared][upstream] with a Web GUI on
top of the unchanged tunnel core.**

Use a Cloudflare Tunnel to remotely connect to Home Assistant without opening
any ports — and configure the whole thing from your browser instead of a YAML
options page and log-tab archaeology.

## What you get

Everything the original Cloudflared add-on does, behaving identically:

- Local-managed tunnels (created by the add-on) and remote-managed tunnels
  (`tunnel_token` from the Cloudflare dashboard).
- The exact same Supervisor options schema: `external_hostname`,
  `additional_hosts`, `tunnel_name`, `catch_all_service`,
  `nginx_proxy_manager`, `post_quantum`, `tunnel_token`, `run_parameters`,
  `log_level`.
- The exact same log output in the Home Assistant Log tab.

Plus a **Web GUI**, served through Home Assistant Ingress (sidebar panel,
protected by your HA login, zero extra ports):

| Page | What it does |
|------|--------------|
| **Dashboard** | Live tunnel status (edge connections), add-on state, one-click restart |
| **Setup** | Guided first run — the Cloudflare authorization URL appears as a clickable link instead of being buried in the log |
| **Config** | Edit every add-on option; saved through the Supervisor API so the HA configuration page and the GUI always stay in sync |
| **Logs** | Live log stream (same content as the HA Log tab) with filter and download |

The Supervisor options remain the **single source of truth**: whatever you
save in the GUI shows up on the HA add-on configuration page and vice versa.

## Installation

1. Add this repository to your Home Assistant add-on store:

   [![Open your Home Assistant instance and show the add add-on repository dialog with a specific repository URL pre-filled.](https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2FWOOWTECH%2FWoow_ha_cloudflare_tunnel_webgui)

   Or manually: **Settings → Add-ons → Add-on Store → ⋮ → Repositories** and
   add `https://github.com/WOOWTECH/Woow_ha_cloudflare_tunnel_webgui`

2. Install the **Cloudflared Web GUI** add-on and start it.

3. Open the Web GUI (the add-on's **OPEN WEB UI** button or the sidebar
   panel) and follow the Setup page. That's it — hostnames, routes, and the
   Cloudflare authorization all happen in the browser.

For all configuration details see the [add-on documentation](cloudflared/DOCS.md)
— it is inherited from upstream and applies unchanged.

## How it differs from upstream

This fork deliberately keeps the tunnel core untouched (same s6 services,
same bash scripts, same cloudflared invocation) so upstream releases can be
merged with a plain `git merge`. The additions:

- A `webgui` s6 service (FastAPI + Vue 3) running alongside the tunnel,
  exposed via Ingress on the internal port 8099.
- `hassio_role: manager` so the GUI can read/write the add-on's own options
  and restart it through the Supervisor API.
- One behavioral change: with a completely **empty** configuration the
  original add-on exits fatally; this fork keeps the GUI reachable (tunnel
  stopped) so first-time setup can happen in the browser. Any saved
  configuration → behavior identical to upstream.

## Architecture

```
┌─ Add-on container ─────────────────────────────────────────────┐
│  s6-overlay                                                    │
│   ├── prepare (oneshot, forked as-is): validate → login →      │
│   │     create tunnel → build config.json → route DNS          │
│   ├── cloudflared (main service, forked as-is): runs tunnel,   │
│   │     stdout → HA Log tab                                    │
│   └── webgui (new, FastAPI :8099 behind HA Ingress)            │
│         ├── Supervisor API: options read/write, restart,       │
│         │     log stream (→ ring buffer → WebSocket)           │
│         ├── login-URL capture from the log stream              │
│         └── tunnel status via cloudflared metrics :36500       │
└────────────────────────────────────────────────────────────────┘
```

## Development

```bash
# Backend (needs Python 3.12+)
cd cloudflared/webgui
python3 -m venv .venv && .venv/bin/pip install -r backend/requirements.txt
WEBGUI_DEV=1 WEBGUI_STATIC=$PWD/frontend/dist \
  .venv/bin/python -m uvicorn backend.main:app --port 8099

# Frontend (needs Node 22+)
cd cloudflared/webgui/frontend
npm install && npm run dev     # dev server proxies /api to :8099
npm run build                  # type-checks + builds to dist/

# Full add-on image
docker build cloudflared/ -t cloudflared-webgui:dev
```

## Syncing with upstream

```bash
git remote add upstream https://github.com/homeassistant-apps/app-cloudflared.git
git fetch upstream
git merge upstream/main   # conflicts only appear in files we deliberately changed
```

## Credits & license

MIT — see [LICENSE.md](LICENSE.md).

The tunnel core is the work of [homeassistant-apps/app-cloudflared][upstream]
(originally by [Tobias Brenner][brenner-tobias]); the Web GUI is by
[WOOWTECH](https://github.com/WOOWTECH), based on
[Woow_cloudflare_tunnel_webgui][woow-standalone] (the standalone
Docker/Podman variant of this GUI).

[upstream]: https://github.com/homeassistant-apps/app-cloudflared
[brenner-tobias]: https://github.com/brenner-tobias
[woow-standalone]: https://github.com/WOOWTECH/Woow_cloudflare_tunnel_webgui

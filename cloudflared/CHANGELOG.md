# Changelog

## 1.0.0

First release of **Cloudflared Web GUI** — a fork of
[homeassistant-apps/app-cloudflared](https://github.com/homeassistant-apps/app-cloudflared)
with a Web GUI on top of the unchanged tunnel core.

### Added

- Web GUI served through Home Assistant Ingress (sidebar panel, protected by
  HA login, no extra port).
  - Dashboard: live tunnel status (metrics `/ready`), add-on state, restart.
  - Setup wizard: captures the `cloudflared tunnel login` authorization URL
    from the log and presents it as a clickable link.
  - Config: full editor for all add-on options, read/written through the
    Supervisor API — the HA configuration page and the GUI always stay in
    sync (the Supervisor options remain the single source of truth).
  - Logs: live WebSocket stream of the add-on log (same content as the HA
    Log tab), with filter and download.

### Changed (vs upstream)

- When started with a completely empty configuration, the add-on no longer
  exits fatally; the Web GUI stays up (tunnel stopped) so first-time setup
  can be done in the browser. With any configuration present, behavior is
  identical to upstream.
- `hassio_role: manager` + Ingress enabled in `config.yaml` (required for
  the GUI to manage the add-on's own options).

All tunnel functionality, configuration options, and log output are
inherited unchanged from upstream app-cloudflared (based on upstream
cloudflared 2026.7.3).

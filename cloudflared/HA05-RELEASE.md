# HA05 source delivery and candidate provenance

This PR proposes 1.0.5. Existing options/schema, ports, architectures, image name,
ingress trust boundary and token keep/remove semantics are unchanged. No data or
options migration is needed. Errors retain loc/type/msg and HTTP status, but drop
input/ctx, pasted values and raw Supervisor error prose.

Five runtime files exactly match tested candidate source
`WOOWTECH/Woow_HA_App_Store@fbdd93a0b06223f96e0e2727ad20880a0b8fc13f`:
`rootfs/run.sh`, `rootfs/etc/s6-overlay/s6-rc.d/prepare/run.sh`, and
`webgui/backend/{main,models,supervisor}.py`. This PR also carries main's Alpine
yq-go 4.53.3-r2 pin; candidate overlay builds reused the pinned 1.0.4 base.
A full CI rebuild is a distinct artifact, not the previously tested image.

## Evidence scope

- Isolated actual HTTP/WS server: baseline 7 disclosure failures; patched artifact
  15/15, marker count 0. Synthetic Supervisor, not live HA.
- Owned HAOS candidate under real Supervisor: 19 HTTP/WS cases and INFO/DEBUG/TRACE
  passed; HTTP/WS-to-INFO retest passed after fixing the inactive Supervisor
  error-state oracle. Each run restored image/options/data/policy.
- Main Chrome at `/app/local_cloudflared_ac1019`: Dashboard, Config, Logs and Setup
  render passed, secret-pattern count 0, navigation only. Save/Restart, explicit
  WS reconnect and real tunnel connectivity were not tested in that browser window.
  Wizard labels do not prove a connected tunnel.
- Official running addon was not upgraded; its acceptance remains FAIL per main.
  Historical 59 tests were not rerun to inflate evidence.

## Candidate identities

Existing immutable amd64 candidate version: `1.0.5-ha05.20261022.1`.
Local OCI manifest: `sha256:290a8f3e40caa3725dd59a28f397560e16c930b1002bd0d331f55c249ffda4a2`.
HAOS source-equivalent image config ID:
`sha256:cf604e5d06a17e23c851e0514144b5e26c656559daf93892ae13d13e182d3b62`.
These are distinct builds; a config ID is not a registry manifest digest.
Candidate evidence is amd64 only. PR CI separately builds both architectures in
test mode. No registry publication or official deployment is asserted here.

## Release boundary and rollback

Current AGENTS.md and Store SOP specify PR plus required architecture checks,
with zero required approvals and no additional human-review gate. Old upstream
CONTRIBUTING sign-off wording conflicts with current explicit WOOW release rules.
Merging this version-bump PR triggers production image/Release/Store publication.
Do not invoke workflow_dispatch for a candidate: non-PR paths publish images.
This draft is source review, not a merge or release instruction.

Candidate publication must use a new non-stable/non-latest tag and record the
verified remote manifest digest, refusing existing tags and ambiguous registry
errors. Do not point a running addon at it. Never silently promote the previously
tested overlay image as a source CI build.

Before any official upgrade, prepare exact installed image/version and a
Supervisor backup scoped to that addon, keeping options private. Upgrade restarts
the official tunnel and ingress. Roll back through supported Supervisor
version/image plus matching backup, then verify original options, health, tunnel
reachability and other apps. Never reuse owned-candidate data backup or tag
manipulation for the official addon. The old version retains its disclosure defect;
rollback does not erase historical logs.

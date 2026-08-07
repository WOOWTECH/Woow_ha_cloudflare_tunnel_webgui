# Cloudflared Web GUI — Home Assistant Add-on

[English](README.md)

**Fork 自 [homeassistant-apps/app-cloudflared][upstream]，通道本體原封不動，
外加一層 Web GUI。**

用 Cloudflare Tunnel 遠端連回 Home Assistant，不用開任何 port——而且整個設定
流程都在瀏覽器裡完成，不必再到 YAML 設定頁與 Log 分頁裡挖授權連結。

## 功能

原版 Cloudflared add-on 的所有功能，行為完全一致：

- 本地管理通道（由 add-on 建立）與遠端管理通道（Cloudflare Dashboard 的
  `tunnel_token`）。
- 完全相同的 Supervisor 選項 schema：`external_hostname`、
  `additional_hosts`、`tunnel_name`、`catch_all_service`、
  `nginx_proxy_manager`、`post_quantum`、`tunnel_token`、`run_parameters`、
  `log_level`。
- HA Log 分頁的記錄輸出完全相同。

再加上 **Web GUI**，透過 Home Assistant Ingress 提供（側邊欄面板、由 HA
登入把關、零額外 port）：

| 頁面 | 功能 |
|------|------|
| **Dashboard** | 即時通道狀態（edge 連線數）、add-on 狀態、一鍵重啟 |
| **Setup** | 首次設定精靈——Cloudflare 授權網址直接變成可點擊的連結，不用去 log 裡撿 |
| **Config** | 編輯所有 add-on 選項；透過 Supervisor API 儲存，HA 設定頁與 GUI 永遠同步 |
| **Logs** | 即時 log 串流（內容與 HA Log 分頁相同），可過濾、可下載 |

Supervisor options 是**唯一事實來源**：在 GUI 存的設定會出現在 HA 的 add-on
設定頁，反之亦然。

## 安裝

1. 把這個 repository 加入 Home Assistant add-on 商店：

   [![Open your Home Assistant instance and show the add add-on repository dialog with a specific repository URL pre-filled.](https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2FWOOWTECH%2FWoow_ha_cloudflare_tunnel_webgui)

   或手動：**設定 → 附加元件 → 附加元件商店 → ⋮ → 儲存庫**，加入
   `https://github.com/WOOWTECH/Woow_ha_cloudflare_tunnel_webgui`

2. 安裝 **Cloudflared Web GUI** add-on 並啟動。

3. 打開 Web GUI（add-on 的 **OPEN WEB UI** 按鈕或側邊欄面板），照著 Setup
   頁走完即可——主機名稱、路由、Cloudflare 授權全部在瀏覽器裡完成。

完整設定說明見 [add-on 文件](cloudflared/DOCS.md)（承襲上游，內容完全適用）。

## 與上游的差異

這個 fork 刻意不動通道本體（相同的 s6 服務、相同的 bash 腳本、相同的
cloudflared 參數），因此上游發佈新版時可以直接 `git merge` 同步。新增的部分：

- 一個 `webgui` s6 服務（FastAPI + Vue 3）與通道並行，經 Ingress 走內部
  port 8099。
- `hassio_role: manager`，讓 GUI 能透過 Supervisor API 讀寫自己的選項並
  重啟 add-on。
- 唯一的行為差異：設定**完全空白**時，原版會直接致命退出；此 fork 讓 GUI
  保持可連（通道停止），首次設定可以在瀏覽器完成。只要存過任何設定，
  行為與上游完全一致。

## 架構

```
┌─ Add-on 容器 ──────────────────────────────────────────────────┐
│  s6-overlay                                                    │
│   ├── prepare（oneshot，原封 fork）：驗證 → login →              │
│   │     建 tunnel → 產 config.json → 設定 DNS                   │
│   ├── cloudflared（主服務，原封 fork）：跑通道，                   │
│   │     stdout → HA Log 分頁                                    │
│   └── webgui（新增，FastAPI :8099，走 HA Ingress）               │
│         ├── Supervisor API：讀寫 options、重啟、                  │
│         │     log 串流（→ ring buffer → WebSocket）              │
│         ├── 從 log 串流擷取授權網址                                │
│         └── 由 cloudflared metrics :36500 取得通道狀態            │
└────────────────────────────────────────────────────────────────┘
```

## 開發

```bash
# 後端（需 Python 3.12+）
cd cloudflared/webgui
python3 -m venv .venv && .venv/bin/pip install -r backend/requirements.txt
WEBGUI_DEV=1 WEBGUI_STATIC=$PWD/frontend/dist \
  .venv/bin/python -m uvicorn backend.main:app --port 8099

# 前端（需 Node 22+）
cd cloudflared/webgui/frontend
npm install && npm run dev     # dev server 會把 /api 代理到 :8099
npm run build                  # 型別檢查 + 建置到 dist/

# 完整 add-on 影像
docker build cloudflared/ -t cloudflared-webgui:dev
```

## 同步上游

```bash
git remote add upstream https://github.com/homeassistant-apps/app-cloudflared.git
git fetch upstream
git merge upstream/main   # 衝突只會出現在我們刻意改過的檔案
```

## 致謝與授權

MIT——見 [LICENSE.md](LICENSE.md)。

通道本體來自 [homeassistant-apps/app-cloudflared][upstream]（原作者
[Tobias Brenner][brenner-tobias]）；Web GUI 由
[WOOWTECH](https://github.com/WOOWTECH) 開發，基於
[Woow_cloudflare_tunnel_webgui][woow-standalone]（本 GUI 的獨立
Docker/Podman 版本）。

[upstream]: https://github.com/homeassistant-apps/app-cloudflared
[brenner-tobias]: https://github.com/brenner-tobias
[woow-standalone]: https://github.com/WOOWTECH/Woow_cloudflare_tunnel_webgui

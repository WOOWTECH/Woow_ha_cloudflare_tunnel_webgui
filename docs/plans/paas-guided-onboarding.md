# CF Web GUI × AIoT PaaS：訂閱、保護、綁定與部署設計

日期：2026-10-23。基線：HA add-on `6391b24`；PaaS OAuth 與 Security Access 契約核對自 `woow_paas_platform` 原始碼。此文件是實作與驗收依據；每項顯示的「安全」結論都要有可觀測證據。

## 問題與目標

目前 add-on 只能讓使用者手貼 Tunnel token。新手不知道在哪裡開通服務、選方案、設定路由與 Cloudflare Access；也無法分辨「Tunnel 已連線」和「網址已受保護且可用」。目標是以一個引導頁完成 **開通訂閱 → 在 PaaS 設定網域與存取規則 → 授權 add-on → 選擇服務 → 綁定本機 → 部署 → 驗證**，並提供換機、撤權、清理路由時可理解的狀態與動作。

PaaS Portal 擁有價格、付款、路由與 Access 寫入權。add-on 透過 OAuth device flow 取得最小必要的讀取與 Tunnel 綁定權，不能用 Portal cookie 代辦付款，也不能把高權限 PaaS Token 暴露給瀏覽器。

## 使用者流程與頁面

入口保留現有 Dashboard / Setup / Config / Logs，新增「PaaS 連結」主線。首次使用的 Setup 顯示兩個大選項：「使用 WOOW PaaS（建議）」與「自建 Cloudflare（進階）」。已使用 Local/手貼 token 的使用者不被自動遷移。

| 步驟 | 介面只問一件事 | 成功後下一步 | 失敗時指引 |
|---|---|---|---|
| 1 開通 | 選工作區，按「前往 PaaS 開通」，在新分頁選方案並完成訂閱 | 回到此頁按「我已開通，重新整理」 | 未有服務：回 PaaS；欠費/停權：前往訂閱頁 |
| 2 設定保護 | PaaS 中設定公開網址、指向 HA 的來源，以及 Access 的登入方式與允許名單 | add-on 顯示路由摘要與保護檢查 | 未保護、同步未完成、登入方法放寬：顯示紅色阻擋及直達 Access 頁 |
| 3 授權 | 在 PaaS 裝置授權頁輸入短碼並同意 `workspace:read security-access:read security-access:tunnel` | 列出使用者可見工作區及服務 | 逾時可重試；拒絕/權限不足提供明確原因 |
| 4 選擇 | 選一個 Security Access，檢視方案、狀態、網域與已綁裝置 | 按「連結並啟用」 | 已被其他裝置綁定：先到 PaaS 換機/撤權，不能搶綁 |
| 5 部署 | 後端再讀最新狀態與每條路由，安全閘通過才領 token、存 Supervisor options、重啟 | 到結果頁輪詢 | 任一步失敗顯示可重試動作；不得在保護失效時啟動 connector |
| 6 驗證 | 分別顯示訂閱、綁定、Tunnel、DNS/外部 HTTP、Access、來源服務 | 可開啟公開網址 | 各項有「已驗證/失敗/無法判定」與採樣時間，不能混作單一綠燈 |

Portal 目前可用路徑：`https://aiot.woowtech.io/woow#/workspaces`；選定工作區可進 `/woow#/workspace/{workspaceId}` 建立 Security Access；既有服務的概覽 `/woow#/workspace/{workspaceId}/security-access/{saId}/overview`，保護設定 `/access`，路由 `/application`。連結使用固定 PaaS origin 與已驗證的整數 ID 組成，不接受瀏覽器提供任意 URL。若 Portal 日後提供專用開通深連結，可在維持舊連結有效下替換。

### 範例文案

「你要讓 `ha.example.com` 安全連回這台 Home Assistant。先到 PaaS 選方案、建立網址，並設定只有 `alice@example.com` 可登入。回來後選擇剛建立的『家用 HA』，按『連結並啟用』。完成時你會看到：服務有效、Access 已發布、Tunnel 在線、網址實測結果。」

PaaS 服務若有 `ha.example.com` 和 `nas.example.com` 兩條路由，**兩條都必須有 Access 保護且無失效/待發布/未解析 IdP** 才能啟動同一個 Tunnel；不能只檢查 HA 路由而讓 NAS 裸露。`access_configuration_ready` 為 PaaS 的寫入收據，仍需獨立外部探測才可宣稱外界真的需要登入。

## 系統邊界與狀態

1. 授權：後端向 `/oauth2/device_authorization` 申請碼，依 RFC 8628 的 `interval`/`slow_down` 輪詢 `/oauth2/token`。前端只收 user code、核准網址、到期時間；`device_code`、access/refresh token 永不返回。初版沿用平台現有 public client `woow-ha-smart-home`，只請求 Security Access 所需的三個 scope；後續建立專用 `woow-cf-webgui` client 並遷移（避免授權同意頁名稱誤導）。
2. 儲存：OAuth refresh token 與本 add-on 專屬隨機 `instance_uid` 在 `/data` 原子寫入、權限 0600；API 只回遮蔽的帳戶/綁定摘要。刷新 token 不可寫日誌。HA 備份會複製 UID；恢復到新機時必須檢查 `binding_conflict` 與 `connector_count`，顯示換機程序，不能默認為同一台。
3. 預檢：必須有有效訂閱/可部署狀態、非空 tunnel ID、至少一條完整路由、每條 route 的 `is_protected=true`、`access_configuration_ready=true`、`access_protection_lost=false`、`access_publish_pending=false`、`access_unresolved_idp_types` 空，且至少一條明確 allow policy。未知欄位採 fail-closed。此處尚不是 Access 邊緣生效證據。
4. 綁定：呼叫 `GET /api/security-access/accesses/{id}/tunnel-token?instance_uid=...&instance_label=...`，PaaS 以 owner/admin + `security-access:tunnel` 驗證；409 不能覆蓋。保存 token 到 Supervisor，重啟 add-on。若 Supervisor 寫入失敗，刪除剛取得的 binding；若重啟後失敗，保留綁定並提供修復/撤權選項，避免失去追溯。
5. 執行：cloudflared 用 0600 token file，參數列和 raw Supervisor log 不含 token；Local tunnel 的 `TunnelSecret` 也不寫日誌。metrics 只 bind loopback。正常設定頁不得回傳明文 token。
6. 狀態：`未授權 → 待開通 → 待設定保護 → 可連結 → 綁定中 → 已連結/驗證中 → 可用`；另有 `停權/欠費`、`已被別機綁定`、`Access 失效`、`外部無法連通`、`待撤權`。每個中間狀態可重試、可返回 Portal；UI 不顯示沒有證據的成功。
7. 解除：先停止本機 connector，清除 Supervisor token，再用同一 UID 呼叫 binding DELETE；若遠端失敗，顯示待撤權並保留可重試記錄。PaaS Portal 負責刪路由、Access application、DNS 與 Tunnel；GUI 只能顯示清理進度/直達連結，沒有 OAuth 寫入 API 時不能假裝已清除。

## API / 權限 / 錯誤模型

GUI 後端自有 `/api/paas/authorization`、`/authorization/status`、`/workspaces`、`/workspaces/{id}/accesses`、`/accesses/{id}/review`、`/accesses/{id}/connect`、`/connection/status`、`/disconnect`。所有端點仍由現有 Ingress 限制。`connect` 後端從 PaaS 重讀 detail 並驗證；前端的預檢結果不可當成啟動權。第一版回傳 FastAPI 的繁中 `detail`，不包含 token、PaaS 回傳 body 或憑證；401 提醒重新授權，403 說明權限不足，409 說明綁定衝突，5xx 標示無法確認且不部署。目標契約是固定 `code`、繁中 `message`、`next_action`，並對 429 尊重 Retry-After；列入後續工單 14，不把目前的簡單錯誤格式宣稱為已完成。

`GET /api/security-access/workspaces`、`.../workspaces/{id}/accesses`、`.../accesses/{id}`、`.../status` 都是讀；`.../tunnel-token` 有 claim 副作用，即使是 GET 也只在最終「連結」按鈕之後呼叫。不得在畫面輪詢時碰它。

## 測試切面與驗收

依 TDD skill，固定三個公開切面：FastAPI `/api/paas/*` 對假的 PaaS HTTP 服務與假的 Supervisor；真正的 `run.sh` 在 shell stub 的 cloudflared argv 與 log 上檢查機密；Vue 頁面透過使用者操作的瀏覽器流程（可用 Playwright）檢查文案、連結與阻擋。每個 ticket 一個紅→綠循環；不對內部私有函式寫鏡像測試。平台契約用 staging/只讀 live 查證，HAOS VM 的寫入測試只碰專用測試訂閱與網址，記錄清理結果。發布、合併和正式訂閱付款仍循現有專案審核流程。

## 不在本輪假造的能力

平台沒有 OAuth 訂閱/付款、Access 寫入與 DNS 清理 API，所以 add-on 只能用精準深連結與返回後刷新串起操作；若要單頁內直接付款/建路由，需由 PaaS 先提供受限、可稽核的 OAuth API。外部 HTTP 探測可辨識 CF 403/302/登入頁，但不能單靠狀態碼保證 policy 確實限制指定身分；需結合 PaaS Access 狀態與未授權探測，結果保留「無法判定」。

## 工單順序

見 `.scratch/paas-guided-onboarding/issues/`。先把會暴露 token 的執行路徑修好，再接入 OAuth 與訂閱導覽、服務安全預檢、綁定部署、分項驗證，最後處理換機/撤權/DNS 清理與 HAOS VM 實測。每票可單獨展示與回退。

## 2026-10-24 實作與驗證紀錄

- 已在 HA add-on 隔離 worktree 完成工單 01–05 的本機實作：token-file／原始 log 收斂、PaaS 四步引導、device flow、工作區與服務讀取、Access 逐路由 fail-closed 預檢、claim/綁定/Supervisor 寫入/重啟與失敗補償。
- 工單 06–08 部分完成：分項狀態、匿名 HTTPS 外部 probe（公開 DNS IP 釘選、拒絕私有位址、無轉址跟隨）、兩段式解除綁定、OAuth 撤銷、PaaS 清理深連結與 Local DNS 殘留警示。自動 DNS/Access 遠端清理仍需可核對 record ID 和 scoped API；目前不聲稱已刪。
- 已加 10–12：專用 OAuth client、Portal 返回與受限開通 API、可查證的 DNS 清理。目前沿用 `woow-ha-smart-home` public client 的最小 scope，授權同意頁名稱尚待平台配合。
- 已加 14：結構化錯誤、429 重試提示與逐狀態下一步導引；第一版先用繁中訊息與 Portal 直達連結。
- 本機驗證：FastAPI 70 項後端測試、shell token 安全測試、Vue 正式編譯均通過。解除綁定的公開 API 測試覆蓋「按停止後立即釋放」與「新程序啟動但舊 Tunnel 還在跑」兩個拒絕路徑；`run_parameters` 測試覆蓋憑證與 metrics 覆蓋企圖。桌機 1440 px 與手機 390 px 畫面經隔離 mock 資料渲染，手機無水平溢出。
- 只讀現場驗證：`paas-ws-fc59d8a2/svc-f1a3c502-haos` 於 2026-10-24 仍 Running/Ready，原 add-on 為 1.0.4 started；本 worktree 尚未安裝到 VM，也未動原 Tunnel token/訂閱。完整 E2E 需先有可安裝的新 add-on 版本與獨立測試訂閱。PaaS 私有 Git 主遠端被 Cloudflare Access 擋住，本地代理遠端亦無法抓取最新 develop，因此平台端 10–12 未在舊 checkout 上硬改。
- 完整 add-on 映像以 Podman 本機建置成功，容器內首頁與 PaaS 初始 API 回 200。更新 lockfile 後 `npm audit --omit=dev` 為 0 筆；剩餘 3 筆 moderate 都在 Tailwind 3 建置工具鏈，修補指引會升到不相容的 Tailwind 4。
- HAOS VM 隔離驗證：只讀掛載本 worktree 的後端與編譯後前端到新容器，僅監聽 guest `127.0.0.1:18026`，沒有 Supervisor token。首頁及 PaaS 初始 API 回 200；真實 PaaS `/oauth2/device_authorization` 回 200、短碼與官方授權網址，API 沒有回傳 device code。測完已停止、刪除隔離容器與檔案；原 add-on 仍 1.0.4 started。此測試不等於已付款、已授權或已綁定的 E2E。
- GitHub 草稿 PR #6 的第一輪 amd64 與 aarch64 add-on build 檢查均通過；Release 工作因沒有版本升級而跳過。後續修補仍須由 CI 重新確認。

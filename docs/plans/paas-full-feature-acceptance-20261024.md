# CF Web GUI 全功能 × PaaS 方案現場驗收

狀態：可自主執行的正式環境／staging 驗收與清理已完成；Local 官方授權、本人登入與其他未覆蓋項目見文末。接續 SA36 的核心流程驗收，依使用者要求擴大到所有現有頁面、設定、方案與恢復路徑。測試切面沿用已核准的公開 GUI/API、真實 Supervisor、cloudflared 執行程序及外部 HTTPS；每個現場缺陷以公開介面的失敗案例開始 TDD 修正。

## 現場基線

- 原 add-on `1b7b4ce7_cloudflared` 1.0.4，原設定雜湊保存在私人驗收目錄；測試使用另一個 Supervisor 本機 add-on `local_cloudflared_paas_acceptance`。
- PaaS 工作區 5／指定測試帳戶；所有新增物件以 `CFGUI-full-20261024` 命名並登記清理清單。
- 現行 catalog：路由 1／3／6／10 組，各有月繳與年繳（8 主方案），各附 1–10 席變體（80 變體），均有 7 天試用。catalog、價格與配額以本輪公開 API 快照為準。
- 正式環境驗證試用功能與即時 Cloudflare；付款與過期等需要可控時鐘的案例優先使用現有 staging／測試付款設定，不能把管理員直接修改資料當作正常使用者操作。

## 驗收矩陣

| 切面 | 必測行為 | 可觀察證據 |
|---|---|---|
| 方案目錄 | 8 主方案的週期／價格／試用／路由／規則／自訂域配額，80 席次變體對應 | catalog 與 Portal 頁面 |
| 訂閱與配額 | 各級距正常建立、上限、超額拒絕、月年對應、席次、方案變更／降級限制 | 公開 API 回應、前後物件數、GUI 提示 |
| Dashboard | 初始 idle、local/token、啟動中／在線／停止、Supervisor、重新啟動 | 真實 Ingress 瀏覽器、metrics、Supervisor |
| Setup | PaaS/Local 導覽、最小設定、Cloudflare 登入連結、憑證／Tunnel／連線狀態、失敗恢復 | 真實 Ingress；Local zone 授權需官方登入 |
| Config | Token 遮蔽／完整命令貼入／保留／替換／移除；Hostname；Tunnel Name；Additional Hosts 增刪與 chunked；Catch-all/NPM 互斥；PQ；每個 Log Level；Run Parameters；Save／Save & Restart／Reset | 瀏覽器操作、讀回設定、啟動參數、錯誤回應 |
| Logs | 初始歷史、WebSocket 即時、篩選、清除、斷線／重連、重啟恢復；機密不外洩 | 瀏覽器與原始 Docker log（只輸出遮蔽結果） |
| PaaS 授權 | 未授權、等待、拒絕、成功、重試、重新讀服務、撤權、無權限 | 瀏覽器、OAuth 與公開 API |
| 保護預檢 | 無路由、未保護、無登入方式、無 allow、過寬規則、多路由混合、已綁別機、有效訂閱／停權／取消 | GUI 按鈕／原因、API 409、不產生 connector |
| 啟用與恢復 | claim、Supervisor 保存與重啟、同裝置重試、第二裝置衝突、外部 probe、來源不可達、重啟後保留、解除／再綁／撤權 | 真實狀態、外部 HTTPS、所有權資料 |
| 清理 | 路由／DNS／Access／Tunnel、試用取消、0 發票、候選 add-on 與暫存檔、工作階段登出、原服務健康及設定雜湊 | PaaS／Cloudflare GET 收據與原環境比對 |

## 結果記錄規則

每個案例標記 `pass`、`fixed_and_retested`、`fail` 或 `blocked`，附對象、輸入、預期、實際、時間與證據。資料契約檢查、受控失敗注入和真實外部登入分別標示。真實瀏覽器操作使用 Supervisor Ingress session，登入工作階段的取得方式也記錄，不宣稱人工輸入帳密。

私人驗收目錄：`/home/woowtechcluster1/.local/state/cf-gui-acceptance/private/e2e-full-20261024/`。教學網頁只保留已遮蔽的截圖、方案表與結果。遇到需帳戶擁有者完成 Cloudflare zone 授權的步驟，保留真實待授權狀態並請使用者接手該步，其餘驗收繼續。

## 2026-10-24 執行結果

### 實機／正式環境

- 真正透過 Supervisor 安裝候選 add-on，所有瀏覽器操作經 HA Ingress。原正式 add-on 未替換。
- Portal 真實選月／年繳、席次試算、建立試用；裝置授權頁實際拒絕與核准。HA／PaaS 登入工作階段由測試管理權限建立，並非人工輸入密碼。
- 8 主方案各建立 trial，逐一填滿路由／Access policy 額度，驗證 N+1 拒絕；80 席次變體的 catalog 與定價全部核對。1 席、10 席及跨路由相同 Email 去重使用真實服務測試，沒有對每個變體逐一付費。
- 多路由只完成一條保護時阻擋；全部完成後可連結。第二裝置領 token 回 409；已連結不能直接換另一服務。
- 公開網址匿名 302。錯填 HA 埠造成 502；修到現場 80 埠後，未信任代理造成 400。透過 HA HTTP WebSocket API 暫時信任候選 add-on 單一 IP，受限來源 IP 測試得到 HA HTML 200 與 WebSocket auth_required，還原 Email allow policy 後再次 302。HA HTTP 設定已還原並確認。
- QUIC＋Post-Quantum、HTTP/2 經 GUI Save & Restart 真正啟動。程序 argv 不含 token，token 檔 0600，metrics 僅 loopback。
- Config 全欄位保存／讀回、7 log levels、11 允許參數、Reset、token 完整 install command／保留／移除；Logs WebSocket／篩選／下載／清除／斷線重連／auto-scroll。
- 真實 OAuth refresh、解除／再綁／再解除、GUI 撤權；撤權後舊 access token 回 401。解綁後 connector、token 檔消失，但 DNS／Access 保留至 PaaS 刪除。
- 受保護路由拒絕直接改名；未保護且無 connector 的專用路由可改名，舊 DNS 已確認移除。

### Staging（非真實刷卡）

- 使用兩個專用一般 Portal 帳號和專用工作區，不用系統管理者身分冒充租戶權限測試。
- 建立 50,000 測試點數 fixture；實際結束試用扣 800、升級退 800 扣 1,200、降級退 1,200 扣 800。逐筆核對已付發票、貸項與 wallet.transaction。
- 重複 skip-trial 拒絕；零餘額 fixture 不扣款且保留 trial。
- 寬限與停權拒絕新增路由；服務名稱仍可修改。時間 fixture 只作用於專用服務，呼叫 lifecycle 的 single-entity seam，未執行全環境 cron。
- 再以真實 staging Tunnel token 接到測試 HAOS，靜態測試 origin 實際呈現 200 → 超過寬限停權 503 → 已付款有效訂閱復權 200。
- 非成員不可讀；普通 workspace user 可讀但不能改名／領 token。
- 專用 staging 服務已刪、訂閱 close/cancel、帳戶停用、工作區封存、session 登出。試驗帳務留作稽核。

### 現場缺陷與 TDD

1. 422 回傳 token（含跨欄位整個 body）：先重現紅燈，改成僅回 type／loc／msg；驗證器也不插入原值。實機重測通過。
2. 已綁定 PaaS 時仍可從 Config 移除 token：先在候選機重現、立即用正常 reconnect 復原，再補公開 API 紅燈；後端 409、共用 mutation lock、前端受管提示，實機重測通過。
3. 零席方案只顯示泛用保護錯誤：補紅燈／席次理由與用量，實機重測通過。
4. 平台空 IdP 清單仍可 ready（operator 語意為不限制 IdP）。GUI 原本即阻止兩個 login flags 都 false；現在補「登入方式」明確提示及公開 API 測試。

### 最終清理與回歸

- 正式環境 SA37–47 共 11 個服務已刪，訂閱 436–446 全部 cancel，發票及對應 wallet.transaction 均為 0。
- 最後兩個保留至測試結束的 Tunnel 已有 deleted_at、0 connectors；DNS／Access GET 404，改名前舊 DNS 為 0 筆。
- 本次候選 add-on 已卸載、容器和專用暫存檔移除。原 add-on 1.0.4 仍 started／auto boot／watchdog；options SHA-256 與測試前相同。
- HA HTTP 的所有設定值還原；新保存紀錄只有 created_at 不同，pending 為 null。原 PaaS SA20 實際仍 connected，1 connector／4 edge connections。
- OAuth 撤權，正式與 staging 的測試 PaaS session 已登出；私人原始收據移出 web 文件根目錄。
- 本次完整本機回歸 80 tests passed；token shell safety PASS；frontend production build PASS；最後候選實機瀏覽器再驗證 Dashboard 重啟、排錯教學、未指定登入方法 409 及撤權。

### 尚未驗收，不作完成宣稱

- Local 官方 zone 授權須網域擁有者接手；已提出非同步請求。無 token／登入 URL 與設定讀回通過，但 Local Tunnel／DNS、Additional Hosts／chunked、NPM／catch-all 的真實傳輸尚未完成。
- 指定 Email OTP 的實際收碼登入需使用者；已提出非同步請求。來源 IP bypass 測試只證明傳輸，不等於本人登入。Google 使用者登入亦未驗收。
- 自訂網域只有 catalog 配額，未執行部署驗收。
- 流量端點回 success，但 data.available=false、reason=permission；只能確認可用性提示，不能宣稱數據功能通過。
- 各 level／parameter 已保存讀回；不是每一種網路參數組合都做過運行測試。

網頁：`reports/aiot-secure-access-20261020/paas-full-acceptance-20261024.html`。
去機密證據：同目錄 `paas-full-acceptance-20261024.json`。完整機密收據收納於 web 根目錄以外的私人驗收檔案。

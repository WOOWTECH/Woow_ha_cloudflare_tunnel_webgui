# 14: 一致的錯誤與重試導引

**What to build:** 將 add-on 的 PaaS API 錯誤統一為 `code`、繁中 `message`、`next_action`；前端依狀態顯示一個直接可做的下一步。429 尊重 PaaS `Retry-After`，避免短碼輪詢與資料刷新過量。

**Blocked by:** 03: 裝置授權；04: PaaS 服務預檢；05: 連結部署。平台端需核對 429 與錯誤碼契約。

**Status:** ready-for-agent

- [ ] 401/403/409/429/5xx 透過公開 Ingress API 測試，不將 PaaS 原始 body 或憑證傳到瀏覽器。
- [ ] 429 測試證明輪詢尊重 `Retry-After`，頁面顯示可重試時間。
- [ ] 頁面提供「重新授權／到 PaaS 管理權限／解除既有綁定／稍後重試」之一，未知狀態維持阻擋。

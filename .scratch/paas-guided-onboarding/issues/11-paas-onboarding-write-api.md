# 11: PaaS 受限開通 API 與返回 add-on 的接續連結

**What to build:** 使用者從 add-on 開啟 PaaS 後，Portal 預先定位工作區與安全存取方案，完成訂閱/付款/Access 設定後一鍵返回 add-on；日後可由 scoped API 預填建立草稿，但付款仍在 Portal 確認。

**Blocked by:** 02: 從 add-on 導覽到 PaaS 開通訂閱；10: PaaS 專用 CF Web GUI 授權身分。

**Status:** ready-for-agent

- [ ] Portal 支援經簽章或 allowlisted 的 return URL/context，不開放任意跳轉；可預選工作區與服務類型。
- [ ] 受限 OAuth scope 只允許建立待確認草稿與查進度，不可代刷付款或繞過角色、配額與 Access gate。
- [ ] 對已付款、取消、停權、重入同一流程設冪等鍵，避免重複訂閱；經 staging 帳務測試。

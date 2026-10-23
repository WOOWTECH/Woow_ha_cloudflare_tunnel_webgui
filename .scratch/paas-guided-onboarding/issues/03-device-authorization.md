# 03: 授權 add-on 讀取自己的 PaaS 服務

**What to build:** 使用者在 PaaS 裝置頁核准後，GUI 自動顯示可用工作區；可以安全重新授權與登出。

**Blocked by:** 02: 從 add-on 導覽到 PaaS 開通訂閱。

**Status:** implemented locally

- [x] 後端遵守 device flow interval/slow_down/過期，前端不取得 device_code 或 OAuth tokens。
- [x] 只要求工作區讀取、Security Access 讀取與 Tunnel 綁定 scope；refresh token 權限 0600 存在 add-on 資料區。
- [x] 401/403/拒絕/逾時顯示可行動的繁中訊息。

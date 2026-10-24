# 18: Local 模式授權與路由功能現場驗收

**What to build:** 使用者能從無 token 的初始狀態取得 Cloudflare zone 授權，建立 HA／Additional Hosts 路由，理解 Catch-all、NPM 與清理限制。

**Blocked by:** 16: 真實 Ingress 全頁面操作驗收。

**Status:** awaiting domain owner authorization; independent PaaS acceptance completed

- [x] 最小設定、真實登入連結與未授權狀態。
- [ ] Local 登入失敗後恢復與官方 zone 授權。
- [ ] 官方 zone 授權後建立專用 Tunnel／DNS，驗證來源與 chunked 設定。
- [ ] Catch-all／NPM 條件、token 與 Local 切換。
- [ ] 清理測試 DNS／Tunnel，記錄未自動清除的項目。

使用者已收到非同步授權接手請求；尚未有回覆。另有 Email OTP 本人登入請求。測試資源會清理，接手時重新建立短期驗收資源，避免等待期間留下可計費訂閱。

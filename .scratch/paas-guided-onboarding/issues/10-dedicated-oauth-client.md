# 10: PaaS 專用 CF Web GUI 授權身分

**What to build:** PaaS 裝置授權同意頁明確顯示「Woow Cloudflared Web GUI」與所需的三個 Security Access scope；既有授權可平順換到新 client。

**Blocked by:** 03: 授權 add-on 讀取自己的 PaaS 服務；PaaS 最新開發分支可讀且可部署到 staging。

**Status:** ready-for-agent

- [ ] 平台建立專用 public client，僅允許 device_code/refresh_token 與三個 scope；既有資料庫 upgrade 可補 seed。
- [ ] add-on 新版優先使用專用 client；舊 client 的既有連結有明確遷移與重新授權流程。
- [ ] staging 完成授權、刷新、撤銷與錯誤分支；同意頁品牌名稱與權限正確。

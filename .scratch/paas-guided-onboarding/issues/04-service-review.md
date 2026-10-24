# 04: 選擇服務並檢查每條路由的保護

**What to build:** GUI 列出訂閱狀態、網址、路由與保護設定；只在所有路由符合安全條件時顯示可連結。

**Blocked by:** 03: 授權 add-on 讀取自己的 PaaS 服務。

**Status:** implemented locally

- [x] 可選工作區與 Security Access，含停權/未開通與無服務的下一步。
- [x] 任一 route 未保護、發布待確認、保護失效、登入方式放寬或無 allow policy 都阻擋連結。
- [x] 可直達該服務的 PaaS Access/應用路由頁；無 token 時只提供導覽。

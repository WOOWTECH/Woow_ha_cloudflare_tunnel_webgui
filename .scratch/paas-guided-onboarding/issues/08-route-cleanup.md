# 08: 路由與 DNS 清理導覽

**What to build:** 刪除服務或切換 Local/PaaS 模式時，GUI 說清楚哪些 DNS/Access/Cloudflare 物件仍在，並提供 PaaS 的對應清理入口。

**Blocked by:** 06: 分項顯示訂閱、保護與連通結果；07: 安全解除綁定與換機。

**Status:** in progress

- [ ] 不能把「本機 token 已刪」誤顯示成「DNS/Access 已刪」。
- [ ] Local 模式移除 Additional Host 時有 DNS 殘留提示與明確清理/核對步驟。
- [ ] 清理後刷新 PaaS 狀態；無法查證時顯示未知。

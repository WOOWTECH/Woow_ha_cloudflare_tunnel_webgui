# 12: 可查證的 DNS 與 Access 清理

**What to build:** 使用者刪除 Local host 或 PaaS route 後可看到 Cloudflare 遠端實際物件是否仍存在，並能安全清除本套件所建立的對應記錄。

**Blocked by:** 08: 路由與 DNS 清理導覽；PaaS/Cloudflare 授權 API 能提供 record ID 與所有權收據。

**Status:** ready-for-agent

- [ ] 刪除前核對 zone、FQDN、CNAME target、record ID 與本套件建立的所有權；不刪同名但非本套件管理的記錄。
- [ ] Cloudflare 刪除回應、再次查詢、Access application 清理結果分開呈現；失敗可重試且不顯示假成功。
- [ ] Local 模式移除 host 與 PaaS 刪 route 的兩種來源都覆蓋；測試用獨立 zone/hostname 並清理完成。

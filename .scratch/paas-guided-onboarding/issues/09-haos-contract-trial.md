# 09: HAOS 測試 VM 端到端驗收

**What to build:** 在專用測試服務與網址上從 Portal 開通、設定 Access、add-on 授權/綁定/部署/驗證，留下實際證據與完整清理記錄。

**Blocked by:** 06: 分項顯示訂閱、保護與連通結果；08: 路由與 DNS 清理導覽。

**Status:** core live E2E completed; human OTP / Local authorization tracked in ticket 18 and full acceptance report.

- [x] 在隔離測試訂閱上完成正常與阻擋分支，包含未保護、已綁定、停權。
- [x] 比對 PaaS API、Supervisor、Cloudflare/外部 probe 的狀態與時間。
- [x] 刪除測試 DNS/Access/Tunnel 與 binding；既有正式服務不受影響。

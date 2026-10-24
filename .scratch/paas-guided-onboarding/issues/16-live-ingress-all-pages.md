# 16: 真實 Ingress 全頁面操作驗收

**What to build:** 使用者能在 HAOS 的 Dashboard、Setup、Config、Logs、PaaS 頁完成各項操作，重啟後可恢復並得到可理解的錯誤。

**Blocked by:** None (can start immediately).

**Status:** completed for GUI controls; Local runtime tracked in 18

- [x] 真實 Supervisor 安裝與 Ingress 瀏覽器操作。
- [x] 每個設定欄位及操作按鈕的保存、拒絕、重啟、重置。
- [x] 日誌 WebSocket、篩選、清除與重連。
- [x] 發現的缺陷先建立回歸案例再修正與現場重測。


## 2026-10-24 實測更新

已執行之項目及限制見 `docs/plans/paas-full-feature-acceptance-20261024.md`；網頁逐項提供預期／實際／證據層級。不能將保存讀回視為 Local 網路驗收，亦不能將匿名 302 視為 OTP 使用者登入。

# 15: 所有現行 PaaS 方案與配額驗收

**What to build:** 使用者能按方案開通試用，路由、Access 規則、席次及自訂域上限有正確成功與拒絕行為，並可安全變更方案。

**Blocked by:** None (can start immediately).

**Status:** executed — 8 base plans / 80 catalog variants; custom-domain deployment excluded and documented

- [x] 核對 8 主方案及 80 席次變體的 catalog。
- [x] 逐級距驗證上限、超額、月年週期、席次及降級限制。
- [x] 記錄失敗、修正、重測與每筆訂閱的取消結果。


## 2026-10-24 實測更新

已執行之項目及限制見 `docs/plans/paas-full-feature-acceptance-20261024.md`；網頁逐項提供預期／實際／證據層級。不能將保存讀回視為 Local 網路驗收，亦不能將匿名 302 視為 OTP 使用者登入。

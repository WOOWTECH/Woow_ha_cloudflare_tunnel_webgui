# 17: 方案搭配保護、綁定與狀態恢復驗收

**What to build:** 不同方案的服務都能依保護狀態決定是否啟動，並在綁定衝突、來源故障、訂閱不可用時給出正確狀態及恢復方法。

**Blocked by:** 15: 所有現行 PaaS 方案與配額驗收；16: 真實 Ingress 全頁面操作驗收。

**Status:** executed and cleaned; human identity/Local authorization remain in ticket 18

- [x] 授權等待／拒絕／核准／撤權與重新讀取服務。
- [x] 逐項保護阻擋分支、多路由、方案席次與綁定衝突。
- [x] 真實啟用、外部探測、來源故障、解除再綁與訂閱不可用。
- [x] 完成所有測試資源清理，核對原 add-on 設定與健康。


## 2026-10-24 實測更新

已執行之項目及限制見 `docs/plans/paas-full-feature-acceptance-20261024.md`；網頁逐項提供預期／實際／證據層級。不能將保存讀回視為 Local 網路驗收，亦不能將匿名 302 視為 OTP 使用者登入。

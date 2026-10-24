# 19: 現場發現的憑證錯誤回應與受管設定保護

**What to build:** 設定錯誤不得回顯秘密；PaaS 管理憑證必須經正常解除綁定才能換模式。

**Blocked by:** None.

**Status:** implemented and live-retested

- [x] 真實 Ingress 重現 invalid-token／cross-field 422 機密回顯。
- [x] 真實綁定期間 Config 刪 token 回 200；立即正常 reconnect 復原。
- [x] 公開 API 紅燈 → 修正 → 綠燈；不以私有 helper 當唯一驗證。
- [x] 422 保留欄位位置與說明，移除原值／context。
- [x] 受管 token 手動變更回 409；release pending 阻止 config 寫入；mutations 共用 lock。
- [x] Supervisor 重建候選版，實機 422／409、UI 提示與 token 保留均通過。

# 07: 安全解除綁定與換機

**What to build:** 原機可一鍵停用本機連線並解除 PaaS 綁定；新機遇到既有綁定時得到換機指引和衝突提示。

**Blocked by:** 05: 按一下連結並啟用已保護的服務。

**Status:** in progress

- [ ] 停 connector、清本機 token、遠端 release 順序清楚且可重試。
- [ ] 備份還原產生重複 connector 時顯示衝突，不自動搶綁。
- [ ] 已失去 OAuth 權限的撤權提供 PaaS Portal 指引，UI 不宣稱遠端已成功解除。

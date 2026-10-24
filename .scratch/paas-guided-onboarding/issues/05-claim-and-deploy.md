# 05: 按一下連結並啟用已保護的服務

**What to build:** 使用者按下連結後，add-on 重新確認 PaaS 狀態，領取 token，綁定本機並重新啟動；中途失敗可重試或回復。

**Blocked by:** 01: Token 與本機憑證安全執行；04: 選擇服務並檢查每條路由的保護。

**Status:** implemented locally

- [x] connect 端點在領取 token 前再次讀取服務/路由；前端資料不可跳過安全閘。
- [x] 409 已被別機綁定不能搶綁；Supervisor 寫入失敗要解除剛建的 binding。
- [x] 成功後保存最小綁定中繼資料並重啟；重試不會生成第二個實例。

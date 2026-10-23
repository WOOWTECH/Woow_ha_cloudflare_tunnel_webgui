# 06: 分項顯示訂閱、保護與連通結果

**What to build:** 使用者可以看到訂閱、Tunnel、DNS/外部 HTTP、Access、來源服務各自的實測結果和時間，知道問題卡在哪一步。

**Blocked by:** 05: 按一下連結並啟用已保護的服務。

**Status:** in progress

- [ ] 欠費、停權、binding conflict、Access 失效與 Tunnel 離線分開呈現。
- [ ] 外部探測分辨需要登入、公開直達、DNS/網路錯誤與無法判定；不把 Tunnel 在線當成網址安全。
- [ ] 每項狀態有採樣時間與修復連結，不洩漏 session token。

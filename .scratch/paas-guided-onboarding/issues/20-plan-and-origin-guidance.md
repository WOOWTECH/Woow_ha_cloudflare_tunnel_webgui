# 20: 方案席次、登入方式與 HA 來源設定的簡明引導

**What to build:** 新手可明白選路由與席次，並分辨 Access 302、HA origin 502、代理信任 400。

**Blocked by:** 15、16。

**Status:** implemented; acceptance receipts in full report

- [x] 一台 HA／一人：1 組路由＋1 席；顯示已用／最大席次。
- [x] 0 席明確引導選至少 1 席；公開 API TDD 和實機驗證。
- [x] 未明確指定登入方法時，指出需勾選 Email OTP 或 Google。
- [x] 可展開的 HTTP 埠、X-Forwarded-For／Trusted proxies 教學與官方連結。
- [x] 網頁報告提供互動方案試算、實際 502→400→200 排錯案例與搜尋證據。

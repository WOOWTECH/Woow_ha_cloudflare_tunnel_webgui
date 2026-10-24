# 01: Token 與本機憑證安全執行

**What to build:** 使用者開啟高詳細度日誌或檢視程序時，Tunnel token、TunnelSecret 仍不會出現在命令列或原始 add-on 日誌；Tunnel 指標只在本機提供。

**Blocked by:** None (can start immediately).

**Status:** implemented locally

- [x] 遠端 Tunnel 使用權限 0600 的 token file，程序 argv 與 debug log 不含 token。
- [x] 本機 Tunnel 建立時原始 log 不含 TunnelSecret。
- [x] metrics 只綁 loopback；現有 Local/Token 模式仍能啟動。

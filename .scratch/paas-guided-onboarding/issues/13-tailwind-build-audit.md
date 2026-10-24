# 13: 清除 Tailwind 建置鏈的剩餘 audit 警訊

**What to build:** 建置工具鏈沒有已知 npm audit 警訊，且 PaaS 引導與既有四頁在桌機／手機上保持可用。

**Blocked by:** 02: 從 add-on 導覽到 PaaS 開通訂閱。

**Status:** ready-for-agent

- [ ] 評估 Tailwind 4 遷移或可維護的相容修補，消除目前 3 項 moderate 建置依賴警訊。
- [ ] 比對編譯 CSS、桌機與手機版面以及原本 Config/Setup/Logs UI。
- [ ] 重新執行 npm audit、前端編譯與完整 add-on 映像建置。

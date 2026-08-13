# Qiyuan MUD－修仙世界

Python + Pygame 單機修仙 RPG MVP。

## Windows 啟動

1. 安裝 Python 3.10 或更新版本。
2. 在專案目錄執行 `python -m pip install -r Requirements.txt`。
3. 雙擊 `start_game.bat`，或執行 `python Main.py`。

開發模式可雙擊 `start_dev.bat`，或執行 `python dev_runner.py`。

## 開發快捷鍵

- F1：Debug 資訊
- F2：重新載入圖片與音訊
- F3：重新載入 JSON
- F4：重新載入目前 Scene
- F5：寫入 Debug 存檔
- F6：讀取 Debug 存檔

正式存檔位於 `saves/save.json`，Debug 存檔與正式存檔互相隔離。
未處理錯誤會寫入 `logs/error.log`。

## 發布前檢查

執行 `python release_check.py`，再執行：

```text
python -m unittest discover -s tests -v
```

目前 MVP 包含角色建立、九大境界一至九層、修煉、打坐、探索、背包、煉丹、商店、Boss、存讀檔、背景、音樂、Debug 與資源重新載入。

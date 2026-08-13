修仙遊戲開發守則

# Pygame 修仙遊戲－Codex 專案脈絡與開發規範

## 0. Codex 必須先遵守的規則

這是一個既有的 Python + Pygame 修仙 RPG 專案，不是全新專案。

修改任何程式碼前：

1. 先讀取現有專案目錄與 `.py` 檔案。
2. 優先沿用現有程式碼，不要直接整套重寫。
3. 不得任意刪除目前已能正常運作的功能。
4. 修改前先確認該功能由哪個 Scene / System / Object 負責。
5. 一次只處理一個明確功能或問題。
6. 修改後必須檢查：

- import 是否正確
- Python 語法
- Pygame Event
- Scene 切換
- None / KeyError / IndexError
- 檔案不存在
- JSON 損毀
- 重複按鈕事件
7. 不要為了「程式碼更漂亮」大規模重構正常功能。
8. 新功能必須符合目前架構。
9. 優先完成 MVP，不主動增加大型系統。
10. 若發現架構問題，先說明問題與修改範圍，再進行重構。
11. 不得使用 `eval()` 解析存檔或外部資料。
12. 不要把所有功能重新塞回 `Main.py`。
13. UI、遊戲規則、玩家資料必須盡量分離。

---

# 1. 專案定位

類型：

Python + Pygame 單機修仙 RPG。

核心玩法：

建立修士 → 修煉 → 提升等級 → 突破境界 → 探索 → 取得資源 → 裝備/煉丹/商店 → 挑戰 Boss → 取得獎勵 → 繼續成長。

目前目標不是製作大型完整 RPG。

第一階段目標為：

**完成穩定、可遊玩、可存檔、可持續擴充的 MVP 1.0。**

---

# 2. MVP 核心循環

```text
建立角色
    ↓
洞府
    ↓
修煉 / 打坐
    ↓
取得經驗
    ↓
升級 / 境界突破
    ↓
探索秘境
    ↓
取得 EXP / 靈石 / 丹藥 / 裝備
    ↓
背包 / 商店 / 煉丹
    ↓
強化角色
    ↓
世界 Boss
    ↓
戰鬥勝利
    ↓
Boss 掉寶
    ↓
回到洞府
    ↓
繼續循環
```

---

# 3. MVP 必須完成的功能

第一版只完成以下功能：

### 3.1 角色系統

角色包含：

- name
- level
- exp
- realm
- realm_index
- hp
- max_hp
- mp
- max_mp
- spirit_stone
- pill
- weapon
- weapon_atk
- armor
- armor_def
- skill
- skill_power
- bag

---

### 3.2 境界系統

目前境界：

```text
練氣期
築基期
金丹期
元嬰期
化神期
```

暫定每 10 級進入下一境界。

必須防止 realm_index 超出陣列範圍。

---

### 3.3 修煉

修煉隨機取得 EXP。

原始規則：

```text
60% 一般修煉：EXP +10～30
30% 爆擊修煉：EXP +40～80
10% 天道頓悟：EXP +120～200
```

取得 EXP 後執行升級判定。

---

### 3.4 打坐

恢復 MP。

原始規則：

```text
MP +20～50
```

不得超過 max_mp。

---

### 3.5 探索秘境

探索產生隨機事件。

目前事件：

```text
上古傳承
遭遇妖獸
找到丹藥
領悟天地靈氣
發現靈石礦脈
```

探索後可能取得：

- EXP
- 靈石
- 丹藥
- HP 傷害

---

### 3.6 煉丹

原始規則：

```text
消耗：30 靈石
成功率：60%
成功：丹藥 +1
失敗：消耗材料但不取得丹藥
```

---

### 3.7 背包

必須支援：

- 顯示物品
- 選取物品
- 裝備武器
- 裝備防具
- 使用消耗品
- 返回

不得因為空背包而 Crash。

不得使用 CSV 字串模擬 Python List。

---

### 3.8 武器

目前：

```text
木劍      ATK 5
鐵劍      ATK 25
精鋼劍    ATK 50
玄鐵劍    ATK 100
```

---

### 3.9 防具

目前：

```text
布衣      DEF 5
銅衣      DEF 10
鐵衣      DEF 20
金蟬衣    DEF 30
```

---

### 3.10 技能

目前：

```text
火球術    20
土刺術    50
冰箭術    80
雷擊術    100
```

技能攻擊需要消耗 MP。

---

# 4. 世界 Boss

MVP 至少保留一隻 Boss。

目前：

```text
名稱：練氣妖狼
HP：100
攻擊：40
```

玩家戰鬥操作：

```text
攻擊
技能
使用丹藥
逃跑
```

戰鬥必須採回合制。

玩家操作一次後，若 Boss 未死亡，Boss 才反擊。

Boss 死亡後不得再次反擊。

---

# 5. Boss 傷害

基本公式：

```text
玩家受到傷害 = Boss Attack - Player DEF
```

最低傷害：

```text
1
```

不得產生負傷害。

---

# 6. Boss 獎勵

原始獎勵：

```text
EXP +100
靈石 +80
隨機掉寶
```

掉寶：

```text
丹藥
武器
防具
```

必須防止：

```text
Boss死亡
→ reward()
→ Scene 尚未切換
→ reward()
→ reward()
```

因此 Battle 必須有類似：

```text
battle_finished
reward_claimed
```

的狀態控制。

同一場戰鬥只能取得一次獎勵。

---

# 7. 商店

MVP 商店包含：

```text
購買丹藥
出售丹藥
購買/升級武器
購買/升級防具
購買/升級技能
返回
```

所有交易必須先檢查：

```text
靈石是否足夠
物品是否存在
數量是否足夠
```

交易後不得產生：

```text
spirit_stone < 0
pill < 0
```

---

# 8. 天書玉簡

「天書玉簡」是遊戲主要功能中心。

建議 MVP 包含：

```text
天書玉簡
│
├── 修士資訊
├── 儲物袋
├── 修煉
├── 打坐
├── 探索秘境
├── 煉丹
├── 商店
├── 世界 Boss
├── 修煉日誌
├── 存檔
├── 讀檔
└── 返回
```

不需要把所有功能同時做成獨立大畫面。

依現有 UI 設計逐步完成。

---

# 9. 洞府 Home

目前主要 UI 概念：

```text
洞府神仙宅，修仙歲月長
```

畫面包含：

### 修士玉牌

顯示：

```text
名諱
靈根
境界
```

### 修為

顯示：

```text
目前修為 / 下一級需求
```

### 洞府修煉日誌

顯示最近發生事件。

例如：

```text
【天道因果】成功堪破時空，載入前世仙緣進度
```

### 主要按鈕

目前概念：

```text
閉關修煉
前往煉丹
天書玉簡
返回選單
```

---

# 10. Scene 架構

Pygame 不得使用大量 `input()` 控制遊戲。

所有操作改成：

```text
Pygame Event
+
Button
+
Scene
```

建議 Scene：

```text
StartScene
CreateScene
HomeScene
CultivationScene
ExploreScene
BagScene
ShopScene
BattleScene
```

需要時再增加其他 Scene。

---

# 11. 建議專案目錄

```text
CultivationGame/
│
├── main.py
├── settings.py
├── dev_runner.py
│
├── assets/
│   ├── fonts/
│   ├── images/
│   │   ├── background/
│   │   ├── player/
│   │   ├── boss/
│   │   ├── items/
│   │   └── ui/
│   ├── sounds/
│   └── music/
│
├── data/
│   ├── items.json
│   ├── bosses.json
│   └── skills.json
│
├── saves/
│   ├── save.json
│   └── debug_save.json
│
├── objects/
│   ├── player.py
│   ├── boss.py
│   └── item.py
│
├── systems/
│   ├── battle_system.py
│   ├── level_system.py
│   ├── item_system.py
│   └── save_system.py
│
├── scenes/
│   ├── start_scene.py
│   ├── create_scene.py
│   ├── home_scene.py
│   ├── cultivation_scene.py
│   ├── explore_scene.py
│   ├── bag_scene.py
│   ├── shop_scene.py
│   └── battle_scene.py
│
└── ui/
    ├── button.py
    ├── panel.py
    ├── progress_bar.py
    └── dialog.py
```

這是目標架構。

若目前專案已有：

```text
Main.py
Home.py
Button.py
Setting.py
Save_system.py
Item_system.py
Level_system.py
```

不要直接刪除。

先分析現有引用關係，再逐步移動或重構。

---

# 12. 各層責任

## main.py

只負責：

```text
pygame.init()
建立視窗
建立遊戲
Event Loop
update
draw
FPS
結束遊戲
```

禁止把：

```text
商店規則
Boss傷害
EXP計算
掉寶
背包規則
```

重新寫進 main.py。

---

## objects/

負責遊戲實體資料。

例如：

```text
Player
Boss
Item
```

---

## systems/

負責規則。

例如：

```text
BattleSystem
LevelSystem
ItemSystem
SaveSystem
```

---

## scenes/

負責：

```text
畫面
按鈕
事件接收
Scene切換
呼叫System
```

Scene 不應大量直接修改遊戲規則。

---

## ui/

負責通用 UI。

例如：

```text
Button
Panel
ProgressBar
Dialog
```

Button 不得自己執行：

```text
player.exp += 100
```

正確方向：

```text
Button
↓
Scene
↓
System
↓
Player
```

---

# 13. 資料驅動

不要把大量遊戲資料寫死在 Python。

逐步使用 JSON。

例如：

## items.json

```json
{
    "wood_sword": {
        "name": "木劍",
        "type": "weapon",
        "attack": 5,
        "price": 0
    },
    "iron_sword": {
        "name": "鐵劍",
        "type": "weapon",
        "attack": 25,
        "price": 100
    }
}
```

---

## bosses.json

```json
{
    "qi_wolf": {
        "name": "練氣妖狼",
        "hp": 100,
        "attack": 40,
        "exp_reward": 100,
        "spirit_stone_reward": 80
    }
}
```

---

# 14. 存檔系統

舊版使用：

```text
pandas
CSV
```

新版不要繼續使用 CSV 作為正式存檔格式。

原因：

背包 List 寫入 CSV 後容易變成 String。

正式改用：

```text
JSON
```

例如：

```json
{
    "save_version": 1,
    "player": {
        "name": "DaoYou",
        "level": 5,
        "exp": 40,
        "realm": "練氣期",
        "hp": 80,
        "mp": 60,
        "spirit_stone": 300,
        "bag": [
            "iron_sword",
            "pill"
        ]
    }
}
```

---

# 15. 存檔安全要求

所有存檔資料視為「不可信資料」。

讀取時驗證：

```text
資料型態
必要欄位
數值上下限
Item ID
Skill ID
Realm
List
```

例如：

```text
level >= 1
hp >= 0
hp <= max_hp
mp >= 0
mp <= max_mp
spirit_stone >= 0
exp >= 0
```

JSON 損毀時：

```text
捕捉 JSONDecodeError
顯示存檔損毀
不要讓遊戲 Crash
```

---

# 16. 安全性規則

## 禁止 eval()

禁止：

```python
eval(save_data)
```

不得使用 `eval()` 處理：

```text
存檔
設定
背包
JSON
CSV
玩家輸入
```

---

## 固定存檔路徑

不得讓玩家任意輸入存檔路徑。

例如固定：

```text
saves/save.json
```

避免：

```text
../../
```

等路徑問題。

---

## 防止數值異常

所有核心數值必須限制。

例如：

```python
hp = max(0, min(hp, max_hp))
```

同樣概念套用：

```text
HP
MP
EXP
靈石
道具數量
Boss HP
```

---

# 17. Pygame Event 安全

購買、攻擊、使用丹藥等操作：

不要每 Frame 直接依賴：

```python
pygame.mouse.get_pressed()
```

避免按住滑鼠後：

```text
購買
購買
購買
購買
購買
```

優先使用：

```text
pygame.MOUSEBUTTONDOWN
```

一次事件只執行一次操作。

---

# 18. Scene 安全

Scene 切換後：

舊 Scene 不得繼續：

```text
更新
接受點擊
發獎勵
執行戰鬥
```

Scene Manager 必須確保只有目前 Scene：

```text
handle_event()
update()
draw()
```

---

# 19. 圖片與音訊載入

所有 Asset 載入都要考慮：

```text
檔案不存在
檔案損毀
路徑錯誤
```

開發階段建議：

圖片不存在時使用 Placeholder。

不要因為：

```text
boss.png
```

不存在，就讓整個遊戲無法啟動。

---

# 20. 開發模式

新增：

```text
dev_runner.py
```

目標：

使用：

```text
watchdog
```

監控 Python 檔案。

開發時：

```text
修改 .py
↓
Ctrl + S
↓
watchdog 偵測
↓
重新啟動 Pygame
↓
立即看到新版
```

正式執行：

```text
python main.py
```

開發執行：

```text
python dev_runner.py
```

---

# 21. Debug Mode

未來加入：

```text
F1：Debug資訊
F2：重新載入圖片
F3：重新載入JSON
F4：重新載入Scene
F5：儲存Debug狀態
F6：載入Debug狀態
```

Debug 存檔：

```text
saves/debug_save.json
```

正式存檔與 Debug 存檔必須分開。

---

# 22. 錯誤處理

任何外部檔案讀取都必須使用合理的例外處理。

至少考慮：

```text
FileNotFoundError
JSONDecodeError
PermissionError
ValueError
TypeError
KeyError
```

但不要：

```python
except:
    pass
```

把所有錯誤直接吃掉。

開發模式應該留下可理解的錯誤資訊。

---

# 23. 命名規則

新程式統一：

Python 檔案：

```text
snake_case.py
```

例如：

```text
save_system.py
battle_system.py
home_scene.py
```

Class：

```text
PascalCase
```

例如：

```text
Player
BattleSystem
HomeScene
```

變數與函式：

```text
snake_case
```

例如：

```text
spirit_stone
weapon_attack
calculate_damage()
```

常數：

```text
UPPER_CASE
```

例如：

```text
SCREEN_WIDTH
SCREEN_HEIGHT
FPS
MAX_LEVEL
```

舊程式命名不要一次全部改掉造成 Import 大量失效。

逐步重構。

---

# 24. 第一版暫時禁止擴充

MVP 完成以前，不主動增加：

```text
宗門
靈獸
坐騎
抽卡
拍賣場
多人連線
排行榜
每日簽到
NPC好感度
大型劇情
完整任務系統
五行戰鬥
裝備鍛造
Steam功能
```

除非使用者明確要求。

---

# 25. MVP 開發順序

嚴格按照：

```text
01 現有專案盤點
02 整理目錄
03 Main / Scene Manager
04 UI基礎元件
05 Player
06 Home Scene
07 修煉
08 打坐
09 Level / Realm
10 Explore
11 Item / Bag
12 Shop
13 Battle
14 Boss
15 Reward
16 JSON Save
17 JSON Load
18 Error Handling
19 Dev Runner
20 Debug Mode
21 UI美化
22 音效
23 完整測試
24 MVP 1.0
```

不要跳著大量增加功能。

---

# 26. Codex 第一次收到專案時要做什麼

第一次不要直接修改大量程式碼。

先執行：

### A. 掃描專案

列出：

```text
所有資料夾
所有 .py
所有 JSON
所有圖片
所有音效
```

### B. 建立 Import 關係

找出：

```text
Main
↓
Scene
↓
UI
↓
System
↓
Object
```

目前實際依賴。

### C. 找出問題

分類成：

```text
Critical
High
Medium
Low
```

至少檢查：

```text
程式無法啟動
Import錯誤
Circular Import
不存在的Key
None問題
Index超界
Scene切換
Button重複觸發
存檔問題
檔案路徑
資源載入
Boss重複獎勵
數值異常
```

### D. 回報

先提供：

```text
目前架構
已完成功能
未完成功能
Bug
安全問題
建議修改順序
```

再開始修改。

---

# 27. Codex 修改程式碼的工作方式

每次工作遵守：

```text
讀取相關檔案
↓
確認目前流程
↓
找出問題
↓
最小修改
↓
執行語法檢查
↓
執行遊戲/測試
↓
確認沒有破壞其他功能
↓
回報修改內容
```

不要：

```text
一次修改十幾個無關檔案
```

---

# 28. 測試要求

每完成一個模組至少測試：

### Player

```text
建立角色
初始資料
HP/MP限制
```

### Level

```text
EXP < 100
EXP = 100
EXP > 100
一次升多級
境界突破
最高境界
```

### Bag

```text
空背包
取得物品
裝備
使用
不存在物品
```

### Shop

```text
靈石足夠
靈石不足
物品不足
連續點擊
```

### Battle

```text
普通攻擊
技能
MP不足
丹藥
丹藥不足
逃跑
玩家死亡
Boss死亡
Boss獎勵只取得一次
```

### Save

```text
正常存檔
正常讀檔
沒有存檔
空JSON
損毀JSON
欄位缺失
錯誤資料型態
非法數值
```

---

# 29. MVP 完成標準

只有以下流程全部可以正常完成，才算 MVP：

```text
開啟遊戲
↓
建立角色
↓
進入洞府
↓
修煉
↓
取得EXP
↓
升級
↓
打坐
↓
探索
↓
取得物品
↓
查看背包
↓
裝備
↓
煉丹
↓
商店
↓
Boss戰
↓
取得獎勵
↓
存檔
↓
關閉遊戲
↓
重新開啟
↓
讀取存檔
↓
資料正確恢復
↓
繼續遊戲
```

整個流程不得出現未處理 Exception。

---

# 30. 第二階段預留

MVP 1.0 完成後，再評估：

```text
更多境界
更多Boss
更多秘境
裝備稀有度
裝備強化
功法系統
靈根系統
五行屬性
任務
成就
圖鑑
宗門
靈獸
NPC
劇情
地圖
動畫
粒子特效
完整音樂系統
```

架構需要能支援這些功能，但 MVP 階段不要提前全部實作。

---

# 31. 最重要的設計原則

整個專案維持：

```text
UI
↓
Scene
↓
System
↓
Object
↓
Data
```

各自負責：

```text
UI       = 怎麼顯示
Scene    = 現在在哪個畫面
System   = 遊戲規則
Object   = 遊戲中的角色/物件
Data     = 數值與設定
```

Save System：

```text
Object
↓
序列化
↓
JSON
```

不得再回到：

```text
Main.py
├─ UI
├─ 玩家
├─ Boss
├─ 商店
├─ 背包
├─ 存檔
├─ 戰鬥
└─ 全部混在一起
```

---

# 32. Codex 最終目標

不是追求最多功能。

而是：

**建立一個穩定、清楚、容易除錯、能持續增加內容的 Pygame 修仙 RPG 基礎框架。**

優先順序固定：

```text
能執行
>
不Crash
>
資料正確
>
核心玩法完整
>
架構清楚
>
方便擴充
>
UI美化
>
額外功能
```
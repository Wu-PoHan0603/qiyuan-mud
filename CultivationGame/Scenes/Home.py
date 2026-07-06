# Scenes/Home.py
import pygame
from Ui.Button import Button
from Systems.Level_system import LevelSystem

level_lookup = LevelSystem()

class HomeScene:
    def __init__(self, width, height, font_path):
        self.width = width
        self.height = height
        self.font_path = font_path
        
        # 1. 玩家動態資料
        self.player_name = "未知修士"
        self.spiritual_root = "凡人"
        self.cultivation = 0  # 修為
        self.realm = "凡人境界" # 境界

        # 2. 建立底部三大主導航按鈕 (精簡排版)
        button_y = 610
        button_w = 220
        button_h = 50
        
        self.btn_train = Button(100, button_y, button_w, button_h, "閉關修煉", font_path, 24)
        self.btn_archive = Button(390, button_y, button_w, button_h, "天書玉簡 📜", font_path, 24)
        self.btn_back = Button(680, button_y, button_w, button_h, "返回選單", font_path, 24)

        # 3. 🌟【核心新增】天書玉簡 11 大功能面板控制
        self.show_archive_menu = False
        self.sub_buttons = {}  # 用字典來儲存這 11 個子按鈕，方便 Main.py 直接點名呼叫
        
        # 定義 11 個按鈕的文字與對應的功能標籤 (Action)
        # 我們將它們排成 3 行 4 列的陣列排版
        sub_btn_data = [
            ("修士資訊", "STATUS"),    ("儲物袋", "BAG"),        ("煉丹介面", "ALCHEMY"),  ("深層打坐", "MEDITATE"),
            ("極速修練", "FAST_TRAIN"), ("探索秘境", "EXPLORE"),    ("世界BOSS", "BOSS"),     ("萬寶商店", "SHOP"),
            ("刻印存檔", "SAVE_GAME"),  ("讀取仙緣", "LOAD_GAME"),  ("系統設置", "SETTING")
        ]
        
        # 九宮格起始座標 (放在畫面中央偏上的浮動面板)
        start_x = 160
        start_y = 200
        grid_w = 160  # 子按鈕寬
        grid_h = 45   # 子按鈕高
        gap_x = 15    # 橫向間距
        gap_y = 15    # 縱向間距
        
        for index, (text, action) in enumerate(sub_btn_data):
            row = index // 4  # 每行 4 個
            col = index % 4
            
            x = start_x + col * (grid_w + gap_x)
            y = start_y + row * (grid_h + gap_y)
            
            # 動態建立按鈕，並存在 sub_buttons 字典裡
            btn = Button(x, y, grid_w, grid_h, text, font_path, 18)
            self.sub_buttons[action] = btn

        # 4. 修仙動態日誌暫存區 (維持 6 行容量)
        self.logs = ["【天道指引】修仙洞府已開闢，請道友開始運功修煉。", "", "", "", "", ""]

    def enter_scene(self, name, root):
        self.player_name = name
        self.spiritual_root = root

    def draw_text(self, surf, text, size, x, y, color=(255, 255, 255)):
        font = pygame.font.Font(self.font_path, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        surf.blit(text_surface, text_rect)

    def add_log(self, text):
        max_chars = 21 
        if len(text) > max_chars:
            self.logs.pop(0); self.logs.append(text[:max_chars])
            self.logs.pop(0); self.logs.append("   " + text[max_chars:])
        else:
            self.logs.pop(0); self.logs.append(text)

    def handle_event(self, event):
        return None

    def draw(self, screen):
        # 洞府背景色
        screen.fill((20, 30, 25))
        
        # 頂部裝飾標題
        self.draw_text(screen, "─── 洞府神仙宅，修仙歲月長 ───", 36, self.width // 2, self.height // 15, (140, 200, 180))
        
        # 如果天書玉簡關閉，照常顯示原本的修士玉牌與進度條
        if not self.show_archive_menu:
            # 左側：修士基本盤
            pygame.draw.rect(screen, (35, 45, 40), (50, 150, 400, 350))
            pygame.draw.rect(screen, (100, 150, 120), (50, 150, 400, 350), 2)
            
            self.draw_text(screen, "【 修士玉牌 】", 26, 250, 170, (200, 220, 180))
            self.draw_text(screen, f"名諱：{self.player_name}", 22, 250, 230)
            self.draw_text(screen, f"靈根：{self.spiritual_root}屬性", 22, 250, 280, (120, 220, 160))
            self.draw_text(screen, f"境界：{self.realm}", 22, 250, 330, (230, 180, 100))
            
            # 右側：修煉進度條
            self.draw_text(screen, "【 當前修為累積 】", 24, 700, 180)
            current_max = level_lookup.get_max_cultivation(self.realm)
            self.draw_text(screen, f"{self.cultivation} / {current_max} 點", 28, 700, 220, (255, 255, 255))

            # 右側：修仙日誌看板
            log_box_x = 510; log_box_y = 280; log_box_w = 440; log_box_h = 220
            pygame.draw.rect(screen, (22, 28, 30), (log_box_x, log_box_y, log_box_w, log_box_h))
            pygame.draw.rect(screen, (100, 130, 110), (log_box_x, log_box_y, log_box_w, log_box_h), 1)
            self.draw_text(screen, "─── 洞府修煉日誌 ───", 20, log_box_x + (log_box_w // 2), log_box_y + 12, (130, 170, 150))
            
            start_y = log_box_y + 48; line_height = 26
            for i, log_text in enumerate(self.logs):
                if i == len(self.logs) - 1: text_color = (255, 255, 210)
                elif i == len(self.logs) - 2: text_color = (230, 230, 230)
                elif i >= len(self.logs) - 4: text_color = (150, 160, 150)
                else: text_color = (80, 95, 85)
                font = pygame.font.Font(self.font_path, 15)
                log_surf = font.render(log_text, True, text_color)
                screen.blit(log_surf, (log_box_x + 18, start_y + i * line_height))
        else:
            # 🌟【全新新增】當打開天書玉簡時，繪製覆蓋全畫面的精美選單面板
            panel_x, panel_y, panel_w, panel_h = 120, 140, 760, 420
            pygame.draw.rect(screen, (25, 30, 35), (panel_x, panel_y, panel_w, panel_h)) # 面板底色
            pygame.draw.rect(screen, (180, 150, 100), (panel_x, panel_y, panel_w, panel_h), 2) # 金色鑲邊
            
            self.draw_text(screen, "📜 ─── 大道天書．萬法歸宗 ─── 📜", 26, self.width // 2, panel_y + 15, (220, 190, 130))
            
            # 繪製這 11 個多功能子按鈕
            for btn in self.sub_buttons.values():
                btn.draw(screen)

        # 繪製底部三大主按鈕
        self.btn_train.draw(screen)
        self.btn_archive.draw(screen)
        self.btn_back.draw(screen)

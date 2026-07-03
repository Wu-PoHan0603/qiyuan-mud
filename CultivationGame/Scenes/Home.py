# Scenes/Home.py
import pygame
from Ui.Button import Button

class HomeScene:
    def __init__(self, width, height, font_path):
        self.width = width
        self.height = height
        self.font_path = font_path
        
        # 1. 玩家動態資料 (初始為空，等創角畫面傳進來)
        self.player_name = "未知修士"
        self.spiritual_root = "凡人"
        self.cultivation = 0  # 修為
        self.realm = "凡人境界" # 境界
        
        # 2. 建立洞府畫面的基本按鈕
        btn_width, btn_height = 200, 50
        # 放在畫面右側或下方作為導覽
        self.btn_train = Button(100, 550, btn_width, btn_height, "閉關修煉", font_path, 24)
        self.btn_alchemy = Button(400, 550, btn_width, btn_height, "前往煉丹", font_path, 24)
        self.btn_back = Button(700, 550, btn_width, btn_height, "返回選單", font_path, 24)

    def enter_scene(self, name, root):
        """核心函式：用來接收創角畫面流轉過來的玩家資料"""
        self.player_name = name
        self.spiritual_root = root

    def draw_text(self, surf, text, size, x, y, color=(255, 255, 255)):
        font = pygame.font.Font(self.font_path, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        surf.blit(text_surface, text_rect)

    def handle_event(self, event):
        """處理洞府內的點擊事件"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = pygame.mouse.get_pos()
            
            # 點擊「閉關修煉」
            if self.btn_train.rect.collidepoint(pos):
                self.cultivation += 10
                if self.cultivation >= 100 and self.realm == "凡人境界":
                    self.realm = "練氣期一層"
                    
            # 點擊「前往煉丹」
            elif self.btn_alchemy.rect.collidepoint(pos):
                return "ALCHEMY" # 未來切換到你的 Alchemy.py
                
            # 點擊「返回選單」
            elif self.btn_back.rect.collidepoint(pos):
                return "MENU"
                
        return None

    def draw(self, screen):
        # 洞府背景色 (古風深綠色或深灰色)
        screen.fill((20, 30, 25))
        
        # 頂部裝飾標題
        self.draw_text(screen, "─── 洞府神仙宅，修仙歲月長 ───", 36, self.width // 2, self.height // 15, (140, 200, 180))
        
        # 左側：修士基本盤
        pygame.draw.rect(screen, (35, 45, 40), (50, 150, 400, 350)) # 畫一個資訊框
        pygame.draw.rect(screen, (100, 150, 120), (50, 150, 400, 350), 2)
        
        self.draw_text(screen, "【 修士玉牌 】", 26, 250, 170, (200, 220, 180))
        self.draw_text(screen, f"名諱：{self.player_name}", 22, 250, 230)
        self.draw_text(screen, f"靈根：{self.spiritual_root}屬性", 22, 250, 280, (120, 220, 160))
        self.draw_text(screen, f"境界：{self.realm}", 22, 250, 330, (230, 180, 100))
        
        # 右側：修煉進度條
        self.draw_text(screen, "【 當前修為累積 】", 24, 700, 200)
        self.draw_text(screen, f"{self.cultivation} / 100 點", 28, 700, 250, (255, 255, 255))
        
        # 繪製按鈕
        self.btn_train.draw(screen)
        self.btn_alchemy.draw(screen)
        self.btn_back.draw(screen)

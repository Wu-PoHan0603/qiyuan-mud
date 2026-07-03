import pygame
import random
from Ui.Button import Button

class CreateScene:
    def __init__(self, width, height, font_path):
        self.width = width
        self.height = height
        self.font_path = font_path

        # 1.創角狀態
        self.player_name = "道友"
        # 2.靈根與面板
        self.spiritual_root = random.choice(["金", "木", "水", "火", "土", "雷", "風", "光", "暗"])
        self.attributes = {"氣血": 100, "修為": 0, "悟性": 0}
        # 3.按鈕
        btn_width, btn_height = 200, 50
        btn_x = (width - btn_width) // 2
        self.btn_roll = Button(btn_x, 450, btn_width, btn_height, "重新抽取靈根", font_path, 24)
        self.btn_confirm = Button(btn_x, 540, btn_width, btn_height, "踏入仙途", font_path, 24)

    def draw_text(self, surf, text, size, x, y, color=(255, 255, 255)):
        font = pygame.font.Font(self.font_path, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        surf.blit(text_surface, text_rect)

    def roll_spiritual_root(self):
        """重新抽取靈根"""
        self.spiritual_root = random.choice(["金", "木", "水", "火", "土", "雷", "風", "光", "暗"])
        self.attributes["悟性"] = random.randint(1, 10)  # 隨機生成悟性值

    def handle_event(self, event):
        """處理創角畫面的按鈕點擊"""
        # 改用 MOUSEBUTTONUP (放開滑鼠) 偵測，最安全、最靈敏
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            pos = pygame.mouse.get_pos()
            
            # 1. 點擊「覺醒靈根」
            if self.btn_roll.rect.collidepoint(pos):
                self.roll_spiritual_root()
                return None # 留在原地
                
            # 2. 點擊「踏入仙途」
            elif self.btn_confirm.rect.collidepoint(pos):
                print("【系統提示】收到踏入仙途點擊，發送 HOME 訊號") # 加上這行 Log 方便除錯
                return "HOME"  # 確保這裡回傳的是大寫的 "HOME"
                
        return None       
            
    def draw(self, screen):
        screen.fill((15, 20, 30))  # 清空畫面

        # 畫標題
        self.draw_text(screen, "【 尋仙問道 - 凝聚真我 】", 48, self.width // 2, self.height // 10, (230, 200, 100))
        self.draw_text(screen, f"修士尊號：{self.player_name}", 28, self.width // 2, self.height // 3)
        self.draw_text(screen, f"先天靈根：{self.spiritual_root}屬性", 28, self.width // 2, self.height // 3 + 50, (100, 230, 150))
        self.draw_text(screen, f"初始屬性 ── 氣血：{self.attributes['氣血']} | 悟性：{self.attributes['悟性']}", 22, self.width // 2, self.height // 3 + 120)
        
        # 繪製按鈕
        self.btn_roll.draw(screen)
        self.btn_confirm.draw(screen)
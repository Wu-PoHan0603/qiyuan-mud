# Scenes/Create.py
import pygame
import random
from Ui.Button import Button

class CreateScene:
    def __init__(self, width, height, font_path):
        self.width = width
        self.height = height
        self.font_path = font_path
        
        # 1. 創角狀態
        self.player_name = "道友"  
        self.spiritual_root = random.choice(["金", "木", "水", "火", "土"])
        self.attributes = {"氣血": 100, "修為": 0, "悟性": 0}
        
        # 2. 文字輸入框設定
        self.input_box = pygame.Rect((width - 300) // 2, 260, 300, 45) 
        self.input_active = False  
        self.color_active = (0, 255, 150)   
        self.color_inactive = (100, 100, 100) 
        self.input_box_color = self.color_inactive

        # === 【核心新增】儲存正在輸入、尚未選字的拼音/注音字串 ===
        self.ime_text = "" 

        # 3. 建立功能按鈕
        btn_width, btn_height = 200, 50
        btn_x = (width - btn_width) // 2
        self.btn_roll = Button(btn_x, 480, btn_width, btn_height, "覺醒靈根", font_path, 24)
        self.btn_confirm = Button(btn_x, 560, btn_width, btn_height, "踏入仙途", font_path, 24)

    def draw_text(self, surf, text, size, x, y, color=(255, 255, 255)):
        font = pygame.font.Font(self.font_path, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        surf.blit(text_surface, text_rect)

    def roll_spiritual_root(self):
        self.spiritual_root = random.choice(["金", "木", "水", "火", "土"])
        self.attributes["悟性"] = random.randint(10, 20)

    def handle_event(self, event):
        """處理創角畫面的滑鼠點擊與中英文輸入事件"""
        
        # A. 處理滑鼠點擊
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            pos = pygame.mouse.get_pos()
            
            if self.input_box.collidepoint(pos):
                if not self.input_active:
                    self.input_active = True
                    self.input_box_color = self.color_active
                    # 啟用作業系統的 IME 輸入法視窗
                    pygame.key.start_text_input()
                    # 讓作業系統的選字窗出現在輸入框附近
                    pygame.key.set_text_input_rect(self.input_box)
                    if self.player_name == "道友":
                        self.player_name = ""
            else:
                if self.input_active:
                    self.input_active = False
                    self.input_box_color = self.color_inactive
                    pygame.key.stop_text_input() # 關閉 IME 監聽
                    if self.player_name.strip() == "":
                        self.player_name = "道友"

            # 按鈕判定
            if self.btn_roll.rect.collidepoint(pos):
                self.roll_spiritual_root()
            elif self.btn_confirm.rect.collidepoint(pos):
                if self.player_name.strip() == "":
                    self.player_name = "無名修士"
                pygame.key.stop_text_input() # 離開時確保關閉
                return "HOME"
                
        # B. 【核心新增】利用 IME 捕捉中文輸入法事件
        if self.input_active:
            # 情況 1：玩家正在敲鍵盤，字還在選字盒裡（例如打注音中）
            if event.type == pygame.TEXTEDITING:
                self.ime_text = event.text
                
            # 情況 2：玩家按了空白鍵或 Enter，確認把字送出（字從選字盒跳進遊戲）
            elif event.type == pygame.TEXTINPUT:
                if len(self.player_name) < 8:
                    self.player_name += event.text
                self.ime_text = "" # 清空選字暫存
                
            # 情況 3：處理刪除鍵（退格鍵）與取消選字
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    # 如果選字盒裡沒有英文字母/注音，才刪除正式的名字
                    if self.ime_text == "":
                        self.player_name = self.player_name[:-1]
                    else:
                        # 如果是在打字途中，退格鍵交由系統處理，這裡清空暫存
                        self.ime_text = self.ime_text[:-1]
                elif event.key == pygame.K_RETURN and self.ime_text == "":
                    self.input_active = False
                    self.input_box_color = self.color_inactive
                    pygame.key.stop_text_input()
                    
        return None

    def draw(self, screen):
        screen.fill((15, 20, 30))
        
        draw_text_y = self.height // 10
        self.draw_text(screen, "【 尋仙問道 - 凝聚真我 】", 48, self.width // 2, draw_text_y, (230, 200, 100))
        self.draw_text(screen, "請用鍵盤輸入或修改你的修士尊號：", 20, self.width // 2, 220, (180, 180, 180))
        
        # 畫出輸入框外框
        pygame.draw.rect(screen, self.input_box_color, self.input_box, 2)
        
        # === 【核心新增】動態渲染：目前名字 + 正在選字的模型文字 ===
        # 把已經確認的名字和還在選字的注音/英文拼在一起顯示
        display_text = self.player_name + self.ime_text
        
        font = pygame.font.Font(self.font_path, 24)
        name_surf = font.render(display_text, True, (255, 255, 255))
        name_rect = name_surf.get_rect()
        name_rect.center = self.input_box.center
        screen.blit(name_surf, name_rect)
        
        # 顯示靈根與先天屬性
        self.draw_text(screen, f"先天靈根：{self.spiritual_root}屬性", 28, self.width // 2, 350, (100, 230, 150))
        self.draw_text(screen, f"初始屬性 ── 氣血：{self.attributes['氣血']} | 悟性：{self.attributes['悟性']}", 22, self.width // 2, 410)
        
        self.btn_roll.draw(screen)
        self.btn_confirm.draw(screen)

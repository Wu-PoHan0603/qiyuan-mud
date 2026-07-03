# Scenes/Menu.py
import pygame
from Ui.Button import create_menu_buttons_list

class MenuScene:
    def __init__(self, width, height, font_path, background_img):
        self.width = width
        self.height = height
        self.font_path = font_path
        self.background_img = background_img
        
        # 動態建立按鈕清單，傳入畫面寬度與字型
        self.start_tick = pygame.time.get_ticks()
        self.buttons = create_menu_buttons_list(width, font_path)
        self.is_started = False  # 用來判斷是否按下任意鍵開始遊戲

    def draw_text(self, surf, text, size, x, y, color=(255, 255, 255)):
        font = pygame.font.Font(self.font_path, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        surf.blit(text_surface, text_rect)

    def handle_event(self, event):
        """處理事件並回傳要切換的場景字串"""
        if not self.is_started:
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONUP:
                self.is_started = True
            return None  # 切換到遊戲場景
        else:
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                pos = pygame.mouse.get_pos()

                for btn in self.buttons:
                    if btn.rect.collidepoint(pos):
                        if btn.text == "開始遊戲":
                            return "CREATE"  # 切換到遊戲場景
                        elif btn.text == "讀取遊戲":
                            return "HOME"  # 切換到設定場景
                        elif btn.text == "離開遊戲":
                            return "QUIT"  # 離開遊戲
        return None  # 沒有切換場景
    
    def draw(self, screen):
        # 畫背景
        screen.blit(self.background_img, (0, 0))

        current_tick = pygame.time.get_ticks()
        if not self.is_started and (current_tick - self.start_tick > 500):
            self.is_started = True
        
        if not self.is_started:
            self.draw_text(screen, "修仙世界", 64, self.width // 2, self.height // 4)
            self.draw_text(screen, "按任意鍵開始", 18, self.width // 2, self.height * 3 // 2)
        else:
            self.draw_text(screen, "修仙世界", 64, self.width // 2, self.height // 6)

            for btn in self.buttons:
                btn.draw(screen)
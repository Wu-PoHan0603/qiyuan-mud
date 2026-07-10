# 按鈕管理 (Button.py)
import pygame


class Button:

    def __init__(self, x, y, width, height, text,
                 font_path=None, font_size=24):

        self.rect = pygame.Rect(x, y, width, height)
        self.current_color = self.normal_color
        self.text = text

        if font_path:
            self.font = pygame.font.Font(font_path, font_size)
        else:
            self.font = pygame.font.SysFont(None, font_size)

        self.normal_color = (70, 70, 70)
        self.hover_color = (120, 120, 120)
        self.text_color = (255, 255, 255)

    # ------------------------------
    # 更新 Hover
    # ------------------------------
    def update(self):

        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.current_color = self.hover_color
        else:
            self.current_color = self.normal_color

    # ------------------------------
    # 是否被點擊
    # ------------------------------
    def is_clicked(self, event):

        return (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        )

    # ------------------------------
    # 畫按鈕
    # ------------------------------
    def draw(self, surface):

        pygame.draw.rect(surface, self.current_color, self.rect)

        pygame.draw.rect(surface, (255,255,255), self.rect,2)

        text = self.font.render(
            self.text,
            True,
            self.text_color
        )

        surface.blit(
            text,
            text.get_rect(center=self.rect.center)
        )

def create_menu_buttons_list(width, font_name, btn_width=255, btn_height=60):
    """利用迴圈動態建立按鈕清單"""
    btn_x = (width - btn_width) // 2
    buttons = []
    
    # 定義每個按鈕的 (文字, Y座標)
    button_data = [
        ("開始遊戲", 350),
        ("讀取遊戲", 440),
        ("離開遊戲", 530)
    ]
    
    for text, btn_y in button_data:
        # 修正：因為寫在 Button.py 內部，直接使用當前的 Button 類別建立物件
        # 同時把 font_name 透過參數傳進來，避免讀不到
        btn = Button(btn_x, btn_y, btn_width, btn_height, text, font_name, 28)
        buttons.append(btn)
        
    return buttons
# Ui/Button.py
import pygame


class Button:
    """共用按鈕元件：update() 處理懸停，is_clicked() 處理事件點擊。"""

    def __init__(
        self,
        x,
        y,
        width,
        height,
        text,
        font_path=None,
        font_size=24,
    ):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font_size = font_size

        if font_path:
            self.font = pygame.font.Font(font_path, font_size)
        else:
            self.font = pygame.font.SysFont(None, font_size)

        self.normal_color = (70, 70, 70)
        self.hover_color = (120, 120, 120)
        self.text_color = (255, 255, 255)
        self.border_color = (255, 255, 255)

        # 必須在 normal_color 建立後再初始化
        self.current_color = self.normal_color

    def update(self):
        """只更新滑鼠懸停效果，不負責點擊判定。"""
        mouse_pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos):
            self.current_color = self.hover_color
        else:
            self.current_color = self.normal_color

    def is_clicked(self, event):
        """使用 pygame 事件判斷滑鼠左鍵是否點擊按鈕。"""
        return (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        )

    def draw(self, surface):
        """繪製按鈕、邊框與文字。"""
        pygame.draw.rect(surface, self.current_color, self.rect)
        pygame.draw.rect(surface, self.border_color, self.rect, 2)

        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)


def create_menu_buttons_list(
    width,
    font_name,
    btn_width=255,
    btn_height=60,
):
    """建立主選單按鈕清單。"""
    btn_x = (width - btn_width) // 2

    button_data = [
        ("開始遊戲", 350),
        ("讀取遊戲", 440),
        ("離開遊戲", 530),
    ]

    return [
        Button(
            btn_x,
            btn_y,
            btn_width,
            btn_height,
            text,
            font_name,
            28,
        )
        for text, btn_y in button_data
    ]

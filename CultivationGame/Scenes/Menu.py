# Scenes/Menu.py
import pygame

from Scenes.BaseScene import BaseScene
from Ui.Button import create_menu_buttons_list
from Ui.visuals import draw_panel, draw_shadow_text


class MenuScene(BaseScene):
    """遊戲主選單場景。"""

    def __init__(self, width, height, font_name, background):
        self.width = width
        self.height = height
        self.font_name = font_name
        self.background = background

        self.buttons = create_menu_buttons_list(
            width=self.width,
            font_name=self.font_name,
        )

        # 方便直接用名稱存取按鈕
        self.btn_start = self.buttons[0]
        self.btn_load = self.buttons[1]
        self.btn_quit = self.buttons[2]

        self.title_font = pygame.font.Font(self.font_name, 64)

    def enter(self):
        print("【場景】進入主選單")

    def exit(self):
        print("【場景】離開主選單")

    def handle_event(self, event):
        if self.btn_start.is_clicked(event):
            return "CREATE"

        if self.btn_load.is_clicked(event):
            return "LOAD"

        if self.btn_quit.is_clicked(event):
            return "QUIT"

        return None

    def update(self):
        for button in self.buttons:
            button.update()

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        draw_panel(screen, (315, 75, 370, 145), (10, 18, 26, 150), (225, 190, 105, 220), 2, 18)
        draw_panel(screen, (350, 320, 300, 300), (10, 18, 26, 135), (180, 150, 90, 180), 1, 14)
        draw_shadow_text(
            screen, self.title_font, "修仙世界", (255, 245, 210),
            (self.width // 2, 150), shadow=(15, 10, 4), offset=(3, 3)
        )

        for button in self.buttons:
            button.draw(screen)

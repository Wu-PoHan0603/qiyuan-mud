# Ui/ArchiveMenu.py
import pygame

from Ui.Button import Button


class ArchiveMenu:
    """天書玉簡彈出選單。

    職責：
    1. 管理天書開啟與關閉狀態。
    2. 建立、更新與繪製子按鈕。
    3. 回傳被點擊的功能代碼。
    """

    def __init__(self, width, height, font_path):
        self.width = width
        self.height = height
        self.font_path = font_path
        self.is_open = False

        self.panel = pygame.Rect(120, 140, 760, 420)
        self.buttons = {}

        button_data = [
            ("修士資訊", "STATUS"),
            ("儲物袋", "BAG"),
            ("煉丹介面", "ALCHEMY"),
            ("深層打坐", "MEDITATE"),
            ("極速修練", "FAST_TRAIN"),
            ("探索秘境", "EXPLORE"),
            ("世界BOSS", "BOSS"),
            ("萬寶商店", "SHOP"),
            ("刻印存檔", "SAVE_GAME"),
            ("讀取仙緣", "LOAD_GAME"),
            ("系統設置", "SETTING"),
        ]

        start_x = 160
        start_y = 200
        button_width = 160
        button_height = 45
        gap_x = 15
        gap_y = 15

        for index, (text, action) in enumerate(button_data):
            row = index // 4
            column = index % 4

            x = start_x + column * (button_width + gap_x)
            y = start_y + row * (button_height + gap_y)

            self.buttons[action] = Button(
                x,
                y,
                button_width,
                button_height,
                text,
                font_path,
                18,
            )

    def open(self):
        self.is_open = True

    def close(self):
        self.is_open = False

    def toggle(self):
        self.is_open = not self.is_open

    def handle_event(self, event):
        """若有子按鈕被點擊，回傳其 action；否則回傳 None。"""
        if not self.is_open:
            return None

        for action, button in self.buttons.items():
            if button.is_clicked(event):
                return action

        return None

    def update(self):
        if not self.is_open:
            return

        for button in self.buttons.values():
            button.update()

    def draw(self, screen):
        if not self.is_open:
            return

        pygame.draw.rect(
            screen,
            (25, 30, 35),
            self.panel,
        )
        pygame.draw.rect(
            screen,
            (180, 150, 100),
            self.panel,
            2,
        )

        title_font = pygame.font.Font(self.font_path, 26)
        title_surface = title_font.render(
            "─── 大道天書．萬法歸宗 ───",
            True,
            (220, 190, 130),
        )
        title_rect = title_surface.get_rect(
            midtop=(self.width // 2, 155)
        )
        screen.blit(title_surface, title_rect)

        for button in self.buttons.values():
            button.draw(screen)

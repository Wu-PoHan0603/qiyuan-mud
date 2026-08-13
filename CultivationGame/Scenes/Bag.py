# Scenes/Bag.py
import pygame

from Scenes.BaseScene import BaseScene
from Ui.Button import Button
from Ui.visuals import draw_panel, draw_shadow_text, draw_wrapped_text


class BagScene(BaseScene):
    """儲物袋場景。

    功能：
    - 顯示所有道具數量
    - 使用聚氣丹增加修為
    - 返回洞府
    """

    def __init__(
        self,
        width,
        height,
        font_path,
        item_system,
        home_scene,
    ):
        self.width = width
        self.height = height
        self.font_path = font_path
        self.item_system = item_system
        self.home_scene = home_scene

        self.message = "神識已探入儲物袋。"
        self.selected_item = "gathering_pill"
        self.items_panel = pygame.Rect(40, 115, 920, 345)
        columns = 3
        rows_per_column = 8
        button_width = 280
        button_height = 32
        gap_x = 20
        gap_y = 8
        start_x = self.items_panel.x + 20
        start_y = self.items_panel.y + 18
        self.item_buttons = {}
        for index, item_id in enumerate(self.item_system.item_database):
            column = index // rows_per_column
            row = index % rows_per_column
            self.item_buttons[item_id] = Button(
                start_x + column * (button_width + gap_x),
                start_y + row * (button_height + gap_y),
                button_width,
                button_height,
                self.item_system.get_item_name(item_id),
                font_path,
                16,
            )

        self.btn_use_gathering = Button(
            380,
            500,
            240,
            55,
            "使用 / 裝備",
            font_path,
            24,
        )
        self.btn_back = Button(
            390,
            600,
            220,
            50,
            "返回洞府",
            font_path,
            24,
        )

    def enter(self):
        self.message = "神識已探入儲物袋。"
        print("【場景】進入儲物袋")

    def exit(self):
        print("【場景】離開儲物袋")

    def handle_event(self, event):
        for item_id, button in self.item_buttons.items():
            if button.is_clicked(event):
                self.selected_item = item_id
                self.message = (
                    f"已選取【{self.item_system.get_item_name(item_id)}】。"
                )
                return None

        if self.btn_use_gathering.is_clicked(event):
            self.use_selected_item()
            return None

        if self.btn_back.is_clicked(event):
            return "HOME"

        return None

    def update(self):
        for item_id, button in self.item_buttons.items():
            count = self.item_system.get_item_count(item_id)
            name = self.item_system.get_item_name(item_id)
            button.text = f"{name} x{count}"
            button.update()
        self.btn_use_gathering.update()
        self.btn_back.update()

    def use_gathering_pill(self):
        self.selected_item = "gathering_pill"
        self.use_selected_item()

    def use_selected_item(self):
        _, message = self.item_system.use_or_equip(
            self.home_scene.player,
            self.selected_item,
            self.home_scene.level_system,
        )
        self.message = message
        self.home_scene.add_log(message)

    def draw_text(
        self,
        surface,
        text,
        size,
        x,
        y,
        color=(255, 255, 255),
    ):
        font = pygame.font.Font(
            self.font_path,
            size,
        )
        draw_shadow_text(surface, font, text, color, (x, y), "midtop")

    def draw(self, screen):
        self.draw_background(screen, (18, 24, 32))

        self.draw_text(
            screen,
            "─── 乾坤儲物袋 ───",
            42,
            self.width // 2,
            45,
            (200, 190, 130),
        )

        draw_panel(
            screen,
            self.items_panel,
            (18, 27, 38, 225),
            (130, 155, 180, 235),
            2,
            10,
        )

        for button in self.item_buttons.values():
            button.draw(screen)

        draw_panel(screen, (190, 450, 620, 43), (15, 20, 28, 215), (175, 145, 85, 220), 1, 8)
        draw_wrapped_text(
            screen, pygame.font.Font(self.font_path, 19), self.message,
            (255, 230, 160), (205, 460, 590, 28), max_lines=1
        )

        self.btn_use_gathering.draw(screen)
        self.btn_back.draw(screen)

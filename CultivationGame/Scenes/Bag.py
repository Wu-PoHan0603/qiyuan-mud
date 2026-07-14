# Scenes/Bag.py
import pygame

from Scenes.BaseScene import BaseScene
from Ui.Button import Button


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

        self.btn_use_gathering = Button(
            380,
            500,
            240,
            55,
            "使用聚氣丹",
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
        if self.btn_use_gathering.is_clicked(event):
            self.use_gathering_pill()
            return None

        if self.btn_back.is_clicked(event):
            return "HOME"

        return None

    def update(self):
        self.btn_use_gathering.update()
        self.btn_back.update()

    def use_gathering_pill(self):
        pill_count = self.item_system.get_item_count(
            "gathering_pill"
        )

        if pill_count <= 0:
            self.message = "聚氣丹不足，無法服用。"
            return

        # 練氣九層已圓滿時，不允許浪費聚氣丹
        current_realm = self.home_scene.player.realm
        current_cultivation = (
            self.home_scene.player.cultivation
        )

        current_max = (
            self.home_scene.level_system
            .get_max_cultivation(current_realm)
        )

        if (
            current_realm == "練氣期第9層"
            and current_cultivation >= current_max
        ):
            self.message = (
                "目前已達練氣九層圓滿，"
                "請使用築基丹突破。"
            )
            return

        removed = self.item_system.remove_item(
            "gathering_pill",
            1,
        )

        if not removed:
            self.message = "聚氣丹使用失敗。"
            return

        (
            new_realm,
            new_cultivation,
            result_message,
        ) = self.home_scene.level_system.add_cultivation(
            current_realm,
            current_cultivation,
            50,
        )

        self.home_scene.player.realm = new_realm
        self.home_scene.player.cultivation = (
            new_cultivation
        )

        self.message = (
            f"服下聚氣丹，{result_message}"
        )

        self.home_scene.add_log(
            f"【丹藥生效】{result_message}"
        )

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
        rendered = font.render(
            text,
            True,
            color,
        )
        rect = rendered.get_rect(
            midtop=(x, y)
        )
        surface.blit(rendered, rect)

    def draw(self, screen):
        screen.fill((18, 24, 32))

        self.draw_text(
            screen,
            "─── 乾坤儲物袋 ───",
            42,
            self.width // 2,
            45,
            (200, 190, 130),
        )

        panel = pygame.Rect(
            180,
            140,
            640,
            300,
        )
        pygame.draw.rect(
            screen,
            (28, 35, 45),
            panel,
        )
        pygame.draw.rect(
            screen,
            (120, 140, 160),
            panel,
            2,
        )

        inventory_rows = [
            ("spirit_stone", "靈石"),
            ("spirit_grass", "靈藥草"),
            ("gathering_pill", "聚氣丹"),
            ("foundation_pill", "築基丹"),
        ]

        start_y = 185

        for index, (item_id, item_name) in enumerate(
            inventory_rows
        ):
            amount = self.item_system.get_item_count(
                item_id
            )

            self.draw_text(
                screen,
                f"{item_name}：{amount}",
                24,
                self.width // 2,
                start_y + index * 55,
                (230, 230, 220),
            )

        self.draw_text(
            screen,
            self.message,
            20,
            self.width // 2,
            455,
            (255, 230, 160),
        )

        self.btn_use_gathering.draw(screen)
        self.btn_back.draw(screen)

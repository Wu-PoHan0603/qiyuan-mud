# Scenes/Alchemy.py
import pygame

from Scenes.BaseScene import BaseScene
from Systems.alchemy_system import AlchemySystem
from Ui.Button import Button
from Ui.visuals import draw_panel, draw_shadow_text, draw_wrapped_text


class AlchemyScene(BaseScene):
    """煉丹場景。

    配方：
    - 聚氣丹：靈石 x30，成功率 60%
    - 築基丹：靈藥草 x5、靈石 x50，成功率 35%
    """

    def __init__(
        self,
        width,
        height,
        font_path,
        item_system,
        alchemy_system=None,
        player_provider=None,
    ):
        self.width = width
        self.height = height
        self.font_path = font_path
        self.item_system = item_system
        self.alchemy_system = alchemy_system or AlchemySystem()
        self.player_provider = player_provider
        self.recipes = self.alchemy_system.RECIPES

        self.selected_recipe = "gathering_pill"
        self.message = "請選擇丹方並開始煉製。"

        self.recipe_buttons = {}
        button_width = 170
        button_height = 42
        start_x = (width - (button_width * 3 + 30 * 2)) // 2
        for index, (recipe_id, recipe) in enumerate(self.recipes.items()):
            column = index % 3
            row = index // 3
            self.recipe_buttons[recipe_id] = Button(
                start_x + column * (button_width + 30),
                145 + row * 55,
                button_width,
                button_height,
                recipe["name"],
                font_path,
                20,
            )
        self.btn_refine = Button(
            390, 505, 220, 55,
            "開始煉丹", font_path, 26
        )
        self.btn_back = Button(
            390, 630, 220, 45,
            "返回洞府", font_path, 24
        )

    def enter(self):
        self.message = "丹爐已點燃，請選擇丹方。"
        print("【場景】進入煉丹房")

    def exit(self):
        print("【場景】離開煉丹房")

    def handle_event(self, event):
        for recipe_id, button in self.recipe_buttons.items():
            if button.is_clicked(event):
                self.selected_recipe = recipe_id
                self.message = f"已選擇【{self.recipes[recipe_id]['name']}】丹方。"
                return None

        if self.btn_refine.is_clicked(event):
            self.refine()
            return None

        if self.btn_back.is_clicked(event):
            return "HOME"

        return None

    def update(self):
        for button in self.recipe_buttons.values():
            button.update()
        self.btn_refine.update()
        self.btn_back.update()

    def refine(self):
        _, self.message = self.alchemy_system.refine(
            self.item_system,
            self.selected_recipe,
        )
        if self.player_provider is not None:
            player = self.player_provider()
            if player is not None:
                player.inventory = self.item_system.get_save_data()
                player.spirit_stone = player.inventory.get("spirit_stone", 0)

    def draw_text(
        self,
        surface,
        text,
        size,
        x,
        y,
        color=(255, 255, 255),
    ):
        font = pygame.font.Font(self.font_path, size)
        draw_shadow_text(surface, font, text, color, (x, y), "midtop")

    def draw(self, screen):
        self.draw_background(screen, (35, 22, 18))

        self.draw_text(
            screen,
            "─── 紫府丹房 ───",
            42,
            self.width // 2,
            45,
            (230, 180, 100),
        )

        self.draw_text(
            screen,
            "選擇丹方",
            26,
            self.width // 2,
            120,
            (220, 220, 200),
        )

        for button in self.recipe_buttons.values():
            button.draw(screen)

        recipe = self.recipes[self.selected_recipe]

        panel = pygame.Rect(250, 325, 500, 145)
        draw_panel(screen, panel, (42, 25, 22, 225), (185, 130, 70, 240), 2, 10)

        self.draw_text(
            screen,
            f"目前丹方：{recipe['name']}",
            24,
            self.width // 2,
            342,
            (255, 220, 150),
        )

        material_text = "材料："
        material_parts = []
        for item_id, amount in recipe["materials"].items():
            item_name = self.item_system.get_item_name(
                item_id
            )
            current = self.item_system.get_item_count(
                item_id
            )
            material_parts.append(
                f"{item_name} {current}/{amount}"
            )

        material_text += "、".join(material_parts)

        self.draw_text(
            screen,
            material_text,
            20,
            self.width // 2,
            388,
        )

        self.draw_text(
            screen,
            f"成功率：{recipe['success_rate']}%",
            20,
            self.width // 2,
            425,
            (180, 220, 180),
        )

        self.btn_refine.draw(screen)
        self.btn_back.draw(screen)

        draw_panel(screen, (210, 570, 580, 48), (26, 18, 16, 220), (180, 125, 70, 220), 1, 8)
        draw_wrapped_text(
            screen, pygame.font.Font(self.font_path, 19), self.message,
            (255, 235, 180), (225, 582, 550, 28), max_lines=1
        )

# Scenes/Alchemy.py
import random

import pygame

from Scenes.BaseScene import BaseScene
from Ui.Button import Button


class AlchemyScene(BaseScene):
    """煉丹場景。

    配方：
    - 聚氣丹：靈藥草 x2、靈石 x10，成功率 70%
    - 築基丹：靈藥草 x5、靈石 x50，成功率 35%
    """

    RECIPES = {
        "gathering_pill": {
            "name": "聚氣丹",
            "materials": {
                "spirit_grass": 2,
                "spirit_stone": 10,
            },
            "success_rate": 70,
        },
        "foundation_pill": {
            "name": "築基丹",
            "materials": {
                "spirit_grass": 5,
                "spirit_stone": 50,
            },
            "success_rate": 35,
        },
    }

    def __init__(
        self,
        width,
        height,
        font_path,
        item_system,
    ):
        self.width = width
        self.height = height
        self.font_path = font_path
        self.item_system = item_system

        self.selected_recipe = "gathering_pill"
        self.message = "請選擇丹方並開始煉製。"

        self.btn_gathering = Button(
            150, 180, 220, 55,
            "聚氣丹", font_path, 24
        )
        self.btn_foundation = Button(
            630, 180, 220, 55,
            "築基丹", font_path, 24
        )
        self.btn_refine = Button(
            390, 480, 220, 60,
            "開始煉丹", font_path, 26
        )
        self.btn_back = Button(
            390, 590, 220, 50,
            "返回洞府", font_path, 24
        )

    def enter(self):
        self.message = "丹爐已點燃，請選擇丹方。"
        print("【場景】進入煉丹房")

    def exit(self):
        print("【場景】離開煉丹房")

    def handle_event(self, event):
        if self.btn_gathering.is_clicked(event):
            self.selected_recipe = "gathering_pill"
            self.message = "已選擇【聚氣丹】丹方。"
            return None

        if self.btn_foundation.is_clicked(event):
            self.selected_recipe = "foundation_pill"
            self.message = "已選擇【築基丹】丹方。"
            return None

        if self.btn_refine.is_clicked(event):
            self.refine()
            return None

        if self.btn_back.is_clicked(event):
            return "HOME"

        return None

    def update(self):
        self.btn_gathering.update()
        self.btn_foundation.update()
        self.btn_refine.update()
        self.btn_back.update()

    def refine(self):
        recipe = self.RECIPES[self.selected_recipe]
        materials = recipe["materials"]

        # 檢查材料
        missing = []
        for item_id, required in materials.items():
            current = self.item_system.get_item_count(item_id)
            if current < required:
                missing.append(
                    f"{self.item_system.get_item_name(item_id)} "
                    f"{current}/{required}"
                )

        if missing:
            self.message = "材料不足：" + "、".join(missing)
            return

        # 扣除材料
        for item_id, required in materials.items():
            self.item_system.remove_item(item_id, required)

        roll = random.randint(1, 100)

        if roll <= recipe["success_rate"]:
            self.item_system.add_item(
                self.selected_recipe,
                1,
            )
            self.message = (
                f"煉丹成功！獲得【{recipe['name']}】x1"
            )
        else:
            self.message = (
                f"煉丹失敗，藥力潰散。"
                f"（成功率 {recipe['success_rate']}%）"
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
        font = pygame.font.Font(self.font_path, size)
        rendered = font.render(text, True, color)
        rect = rendered.get_rect(midtop=(x, y))
        surface.blit(rendered, rect)

    def draw(self, screen):
        screen.fill((35, 22, 18))

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

        self.btn_gathering.draw(screen)
        self.btn_foundation.draw(screen)

        recipe = self.RECIPES[self.selected_recipe]

        panel = pygame.Rect(250, 280, 500, 150)
        pygame.draw.rect(screen, (50, 35, 30), panel)
        pygame.draw.rect(
            screen,
            (170, 120, 70),
            panel,
            2,
        )

        self.draw_text(
            screen,
            f"目前丹方：{recipe['name']}",
            24,
            self.width // 2,
            300,
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
            350,
        )

        self.draw_text(
            screen,
            f"成功率：{recipe['success_rate']}%",
            20,
            self.width // 2,
            390,
            (180, 220, 180),
        )

        self.btn_refine.draw(screen)
        self.btn_back.draw(screen)

        self.draw_text(
            screen,
            self.message,
            20,
            self.width // 2,
            550,
            (255, 235, 180),
        )

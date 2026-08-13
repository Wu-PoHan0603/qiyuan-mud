import pygame

from Scenes.BaseScene import BaseScene
from Systems.shop_system import ShopSystem
from Ui.Button import Button
from Ui.visuals import draw_panel, draw_shadow_text, draw_wrapped_text


class ShopScene(BaseScene):
    def __init__(self, width, height, font_path, item_system, player_provider):
        self.width = width
        self.height = height
        self.font_path = font_path
        self.item_system = item_system
        self.player_provider = player_provider
        self.shop_system = ShopSystem()
        self.selected_item = "gathering_pill"
        self.message = "請選擇商品。"
        self.items_panel = pygame.Rect(40, 105, 920, 300)
        columns = 3
        rows_per_column = 5
        button_width = 280
        button_height = 40
        gap_x = 20
        gap_y = 10
        start_x = self.items_panel.x + 20
        start_y = self.items_panel.y + 20
        self.item_buttons = {}
        for index, item_id in enumerate(self.shop_system.PRICES):
            column = index // rows_per_column
            row = index % rows_per_column
            self.item_buttons[item_id] = Button(
                start_x + column * (button_width + gap_x),
                start_y + row * (button_height + gap_y),
                button_width,
                button_height,
                item_system.get_item_name(item_id), font_path, 17,
            )
        self.btn_buy = Button(180, 430, 190, 50, "購買", font_path, 22)
        self.btn_sell = Button(405, 430, 190, 50, "出售", font_path, 22)
        self.btn_back = Button(630, 430, 190, 50, "返回洞府", font_path, 22)

    def handle_event(self, event):
        for item_id, button in self.item_buttons.items():
            if button.is_clicked(event):
                self.selected_item = item_id
                self.message = f"已選擇【{self.item_system.get_item_name(item_id)}】。"
                return None
        player = self.player_provider()
        if self.btn_buy.is_clicked(event):
            _, self.message = self.shop_system.buy(player, self.item_system, self.selected_item)
        elif self.btn_sell.is_clicked(event):
            _, self.message = self.shop_system.sell(player, self.item_system, self.selected_item)
        elif self.btn_back.is_clicked(event):
            return "HOME"
        return None

    def update(self):
        for item_id, button in self.item_buttons.items():
            price = self.shop_system.PRICES[item_id]
            button.text = f"{self.item_system.get_item_name(item_id)} {price}靈石"
            button.update()
        self.btn_buy.update(); self.btn_sell.update(); self.btn_back.update()

    def draw(self, screen):
        self.draw_background(screen, (28, 24, 35))
        draw_panel(screen, self.items_panel, (24, 18, 30, 205), (205, 165, 90, 230), 2, 12)
        font = pygame.font.Font(self.font_path, 34)
        draw_shadow_text(screen, font, "─── 萬寶商店 ───", (240, 210, 140), (self.width // 2, 60))
        for button in self.item_buttons.values(): button.draw(screen)
        self.btn_buy.draw(screen); self.btn_sell.draw(screen); self.btn_back.draw(screen)
        small = pygame.font.Font(self.font_path, 19)
        stones = self.item_system.get_item_count("spirit_stone")
        draw_panel(screen, (120, 510, 760, 70), (20, 16, 26, 225), (190, 150, 80, 230), 2, 9)
        draw_wrapped_text(
            screen, small, f"靈石：{stones}　{self.message}",
            (245, 235, 195), (145, 526, 710, 44), max_lines=2
        )

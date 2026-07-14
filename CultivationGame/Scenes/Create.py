# Scenes/Create.py
import random

import pygame

from Objects.Player import Player
from Scenes.BaseScene import BaseScene
from Ui.Button import Button


class CreateScene(BaseScene):
    """角色建立場景。"""

    def __init__(self, width, height, font_path):
        self.width = width
        self.height = height
        self.font_path = font_path

        self.player_name = "道友"
        self.spiritual_root = random.choice(
            ["金", "木", "水", "火", "土"]
        )
        self.attributes = {
            "氣血": 100,
            "修為": 0,
            "悟性": random.randint(10, 20),
        }

        self.created_player = None

        self.input_box = pygame.Rect(
            (width - 300) // 2,
            260,
            300,
            45,
        )
        self.input_active = False
        self.color_active = (0, 255, 150)
        self.color_inactive = (100, 100, 100)
        self.input_box_color = self.color_inactive
        self.ime_text = ""

        button_width = 200
        button_height = 50
        button_x = (width - button_width) // 2

        self.btn_roll = Button(
            button_x,
            480,
            button_width,
            button_height,
            "覺醒靈根",
            font_path,
            24,
        )
        self.btn_confirm = Button(
            button_x,
            560,
            button_width,
            button_height,
            "踏入仙途",
            font_path,
            24,
        )

    def enter(self):
        print("【場景】進入創角畫面")

    def exit(self):
        pygame.key.stop_text_input()
        self.input_active = False

    def roll_spiritual_root(self):
        self.spiritual_root = random.choice(
            ["金", "木", "水", "火", "土"]
        )
        self.attributes["悟性"] = random.randint(10, 20)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.input_box.collidepoint(event.pos):
                self.input_active = True
                self.input_box_color = self.color_active
                pygame.key.start_text_input()
                pygame.key.set_text_input_rect(
                    self.input_box
                )

                if self.player_name == "道友":
                    self.player_name = ""
            else:
                self.input_active = False
                self.input_box_color = self.color_inactive
                pygame.key.stop_text_input()

                if not self.player_name.strip():
                    self.player_name = "道友"

        if self.btn_roll.is_clicked(event):
            self.roll_spiritual_root()
            return None

        if self.btn_confirm.is_clicked(event):
            name = self.player_name.strip() or "無名修士"

            self.created_player = Player(
                name=name,
                spiritual_root=self.spiritual_root,
                realm="凡人境界",
                cultivation=0,
                spirit_stone=10,
                hp=100,
                mp=100,
            )
            return "HOME"

        if self.input_active:
            if event.type == pygame.TEXTEDITING:
                self.ime_text = event.text

            elif event.type == pygame.TEXTINPUT:
                if len(self.player_name) < 8:
                    self.player_name += event.text
                self.ime_text = ""

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    if self.ime_text:
                        self.ime_text = self.ime_text[:-1]
                    else:
                        self.player_name = self.player_name[:-1]

                elif event.key == pygame.K_RETURN:
                    self.input_active = False
                    self.input_box_color = self.color_inactive
                    pygame.key.stop_text_input()

        return None

    def update(self):
        self.btn_roll.update()
        self.btn_confirm.update()

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
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(midtop=(x, y))
        surface.blit(text_surface, text_rect)

    def draw(self, screen):
        screen.fill((15, 20, 30))

        self.draw_text(
            screen,
            "【 尋仙問道 - 凝聚真我 】",
            48,
            self.width // 2,
            70,
            (230, 200, 100),
        )
        self.draw_text(
            screen,
            "請輸入修士尊號：",
            20,
            self.width // 2,
            220,
            (180, 180, 180),
        )

        pygame.draw.rect(
            screen,
            self.input_box_color,
            self.input_box,
            2,
        )

        display_text = self.player_name + self.ime_text
        font = pygame.font.Font(self.font_path, 24)
        name_surface = font.render(
            display_text,
            True,
            (255, 255, 255),
        )
        name_rect = name_surface.get_rect(
            center=self.input_box.center
        )
        screen.blit(name_surface, name_rect)

        self.draw_text(
            screen,
            f"先天靈根：{self.spiritual_root}屬性",
            28,
            self.width // 2,
            350,
            (100, 230, 150),
        )
        self.draw_text(
            screen,
            (
                f"初始屬性 ── 氣血：{self.attributes['氣血']} "
                f"| 悟性：{self.attributes['悟性']}"
            ),
            22,
            self.width // 2,
            410,
        )

        self.btn_roll.draw(screen)
        self.btn_confirm.draw(screen)

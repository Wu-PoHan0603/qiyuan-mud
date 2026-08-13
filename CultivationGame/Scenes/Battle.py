import pygame

from Scenes.BaseScene import BaseScene
from Systems.Battle_system import BattleSystem
from Ui.Button import Button
from Ui.Progressbar import ProgressBar
from Ui.visuals import draw_panel, draw_shadow_text, draw_wrapped_text


class BattleScene(BaseScene):
    def __init__(self, width, height, font_path, item_system, player_provider, background_provider=None):
        self.width = width; self.height = height; self.font_path = font_path
        self.item_system = item_system; self.player_provider = player_provider
        self.background_provider = background_provider
        self.system = BattleSystem()
        self.boss = self.system.create_boss_for_player(self.player_provider())
        self.message = f"{self.boss.name}攔住了去路。"
        labels = (("攻擊", 130), ("技能", 330), ("丹藥", 530), ("逃跑", 730))
        self.buttons = {text: Button(x, 560, 140, 50, text, font_path, 22) for text, x in labels}
        self.back = Button(390, 630, 220, 45, "返回洞府", font_path, 20)
        self.boss_hp_bar = ProgressBar(200, 135, 600, 22, (180, 55, 55))
        self.player_hp_bar = ProgressBar(200, 235, 600, 20, (55, 180, 80))
        self.player_mp_bar = ProgressBar(200, 262, 600, 16, (65, 105, 210))

    def enter(self):
        player = self.player_provider()
        if self.background_provider is not None:
            key = "BATTLE_DEMON" if player.realm_index >= 4 else "BATTLE"
            self.set_background(self.background_provider(key), 90)
        if player.hp <= 0:
            self.system.recover_after_defeat(player)
        self.boss = self.system.create_boss_for_player(player)
        self.message = f"{self.boss.name}攔住了去路。"

    def handle_event(self, event):
        player = self.player_provider()
        if self.buttons["攻擊"].is_clicked(event): result = self.system.attack(player, self.boss)
        elif self.buttons["技能"].is_clicked(event): result = self.system.use_skill(player, self.boss)
        elif self.buttons["丹藥"].is_clicked(event): result = self.system.use_pill(player, self.boss, self.item_system)
        elif self.buttons["逃跑"].is_clicked(event):
            self.system.flee()
            self.system.recover_after_defeat(player)
            return "HOME"
        elif self.back.is_clicked(event) and self.system.battle_finished:
            self.system.recover_after_defeat(player)
            return "HOME"
        else: return None
        _, self.message = result
        if self.boss.is_dead:
            ok, reward = self.system.claim_reward(player, self.boss, self.item_system)
            if ok: self.message += " " + reward
        return None

    def update(self):
        for button in self.buttons.values(): button.update()
        self.back.update()

    @staticmethod
    def wrap_message(text, max_chars=42):
        if not text:
            return [""]
        return [
            text[index:index + max_chars]
            for index in range(0, len(text), max_chars)
        ]

    def draw(self, screen):
        self.draw_background(screen, (35, 18, 18)); player = self.player_provider()
        draw_panel(screen, (155, 70, 690, 225), (20, 13, 16, 205), (190, 105, 80, 230), 2, 12)
        draw_panel(screen, (145, 300, 710, 205), (18, 12, 15, 220), (155, 95, 75, 220), 2, 10)
        self.boss_hp_bar.set_value(self.boss.hp, self.boss.max_hp)
        self.player_hp_bar.set_value(player.hp, player.max_hp)
        self.player_mp_bar.set_value(player.mp, player.max_mp)
        self.boss_hp_bar.draw(screen)
        self.player_hp_bar.draw(screen)
        self.player_mp_bar.draw(screen)
        font = pygame.font.Font(self.font_path, 28)
        small = pygame.font.Font(self.font_path, 19)
        status_lines = (
            f"{self.boss.name} HP {self.boss.hp}/{self.boss.max_hp}",
            f"{player.name} HP {player.hp}/{player.max_hp} MP {player.mp}/{player.max_mp}",
        )
        for index, text in enumerate(status_lines):
            draw_shadow_text(
                screen, font, text, (245, 225, 195),
                (self.width // 2, 100 + index * 100)
            )
        draw_wrapped_text(
            screen, small, self.message, (245, 225, 195),
            (175, 320, 650, 165), line_spacing=5, max_lines=6
        )
        for button in self.buttons.values(): button.draw(screen)
        if self.system.battle_finished: self.back.draw(screen)

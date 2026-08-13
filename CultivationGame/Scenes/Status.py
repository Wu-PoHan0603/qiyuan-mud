import pygame

from Scenes.BaseScene import BaseScene
from Ui.Button import Button
from Ui.visuals import draw_panel, draw_shadow_text


class StatusScene(BaseScene):
    """Read-only character status view."""

    def __init__(self, width, height, font_path, player_provider, level_system):
        self.width = width
        self.height = height
        self.font_path = font_path
        self.player_provider = player_provider
        self.level_system = level_system
        self.btn_back = Button(390, 620, 220, 50, "返回洞府", font_path, 24)

    def handle_event(self, event):
        if self.btn_back.is_clicked(event):
            return "HOME"
        return None

    def update(self):
        self.btn_back.update()

    def _draw_text(self, screen, text, size, x, y, color=(235, 235, 225)):
        font = pygame.font.Font(self.font_path, size)
        draw_shadow_text(screen, font, text, color, (x, y), "topleft")

    def draw(self, screen):
        self.draw_background(screen, (18, 25, 32))
        draw_panel(screen, (115, 105, 770, 440), (15, 22, 30, 220), (185, 155, 90, 230), 2, 12)
        self._draw_text(screen, "修士資訊", 40, 410, 45, (230, 190, 110))
        player = self.player_provider()
        if player is None:
            self._draw_text(screen, "尚未建立角色。", 26, 400, 260)
            self.btn_back.draw(screen)
            return

        max_cultivation = self.level_system.get_max_cultivation(player.realm)
        rows = (
            ("姓名", player.name),
            ("靈根", player.spiritual_root),
            ("境界", player.realm),
            ("修為", f"{player.cultivation} / {max_cultivation}"),
            ("等級 / 經驗", f"{player.level} / {player.exp}"),
            ("氣血", f"{player.hp} / {player.max_hp}"),
            ("法力", f"{player.mp} / {player.max_mp}"),
            ("靈石", str(player.spirit_stone)),
            ("武器", f"{player.weapon}（攻擊 {player.weapon_atk}）"),
            ("防具", f"{player.armor}（防禦 {player.armor_def}）"),
            ("技能", f"{player.skill}（威力 {player.skill_power}）"),
        )
        for index, (label, value) in enumerate(rows):
            column = index // 6
            row = index % 6
            x = 170 + column * 390
            y = 130 + row * 68
            self._draw_text(screen, f"{label}：", 22, x, y, (190, 165, 110))
            self._draw_text(screen, str(value), 22, x + 135, y)
        self.btn_back.draw(screen)

import pathlib
import tempfile
import unittest
from unittest.mock import Mock

import pygame

from Objects.GameSettings import GameSettings
from Scenes.Alchemy import AlchemyScene
from Scenes.Bag import BagScene
from Scenes.Battle import BattleScene
from Scenes.Create import CreateScene
from Scenes.Home import HomeScene
from Scenes.Menu import MenuScene
from Scenes.Settings import SettingsScene
from Scenes.Shop import ShopScene
from Scenes.Status import StatusScene
from Systems.Item_system import ItemSystem
from Systems.asset_manager import AssetManager
from Systems.settings_system import SettingsSystem
from Ui.ArchiveMenu import ArchiveMenu
from Ui.Button import Button
from Ui.DebugOverlay import DebugOverlay
from Ui.Progressbar import ProgressBar
from Ui.visuals import draw_panel, draw_shadow_text, draw_wrapped_text, wrap_text


PROJECT_DIR = pathlib.Path(__file__).resolve().parents[1]


class UiReadabilityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()
        pygame.display.set_mode((1, 1))
        cls.font = pygame.font.Font(None, 24)

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    def test_01_panel_blends_with_background(self):
        surface = pygame.Surface((40, 40)); surface.fill((200, 200, 200))
        draw_panel(surface, (5, 5, 30, 30), (0, 0, 0, 128))
        pixel = surface.get_at((20, 20))
        self.assertTrue(80 < pixel.r < 120)

    def test_02_panel_border_is_visible(self):
        surface = pygame.Surface((40, 40)); surface.fill((0, 0, 0))
        draw_panel(surface, (5, 5, 30, 30), border=(255, 200, 100, 255))
        self.assertGreater(surface.get_at((5, 20)).r, 150)

    def test_03_shadow_text_returns_positioned_rect(self):
        surface = pygame.Surface((200, 80))
        rect = draw_shadow_text(surface, self.font, "修仙", (255, 255, 255), (100, 40))
        self.assertEqual(rect.center, (100, 40))

    def test_04_empty_text_wraps_to_one_line(self):
        self.assertEqual(wrap_text("", self.font, 100), [""])

    def test_05_chinese_text_wraps_by_pixel_width(self):
        lines = wrap_text("修仙世界大道長生", self.font, 45)
        self.assertGreater(len(lines), 1)
        self.assertTrue(all(self.font.size(line)[0] <= 45 for line in lines))

    def test_06_latin_text_wraps_by_pixel_width(self):
        lines = wrap_text("Asset reload incomplete", self.font, 70)
        self.assertGreater(len(lines), 1)
        self.assertEqual("".join(lines), "Asset reload incomplete")

    def test_07_wrapped_text_honors_max_lines(self):
        surface = pygame.Surface((200, 100))
        lines = draw_wrapped_text(surface, self.font, "很長的訊息" * 20, (255, 255, 255), (0, 0, 100, 80), max_lines=2)
        self.assertEqual(len(lines), 2)

    def test_08_button_uses_high_contrast_colors(self):
        button = Button(0, 0, 120, 40, "按鈕")
        self.assertGreater(sum(button.text_color), sum(button.normal_color[:3]))
        self.assertNotEqual(button.normal_color, button.hover_color)

    def test_09_button_draws_on_transparent_style(self):
        surface = pygame.Surface((140, 60)); surface.fill((200, 200, 200))
        button = Button(10, 10, 120, 40, "按鈕"); button.draw(surface)
        self.assertNotEqual(surface.get_at((20, 20))[:3], (200, 200, 200))

    def test_10_progress_bar_clamps_below_zero(self):
        bar = ProgressBar(0, 0, 100, 20, (255, 0, 0)); bar.set_value(-5, 100)
        self.assertEqual(bar.ratio, 0)

    def test_11_progress_bar_clamps_above_maximum(self):
        bar = ProgressBar(0, 0, 100, 20, (255, 0, 0)); bar.set_value(500, 100)
        self.assertEqual(bar.ratio, 1)

    def test_12_progress_bar_zero_maximum_is_safe(self):
        bar = ProgressBar(0, 0, 100, 20, (255, 0, 0)); bar.set_value(1, 0)
        bar.draw(pygame.Surface((100, 20))); self.assertEqual(bar.ratio, 0)

    def test_13_archive_panel_draws_only_when_open(self):
        menu = ArchiveMenu(1000, 700, None); surface = pygame.Surface((1000, 700)); surface.fill((1, 2, 3))
        menu.draw(surface); before = surface.get_at(menu.panel.center)
        menu.open(); menu.draw(surface); after = surface.get_at(menu.panel.center)
        self.assertNotEqual(before, after)

    def _make_scenes(self):
        assets = AssetManager(PROJECT_DIR, (1000, 700)); assets.load_all()
        items = ItemSystem(); home = HomeScene(1000, 700, None, item_system=items)
        items.load_save_data(home.player.inventory)
        scenes = [
            MenuScene(1000, 700, None, assets.get_background("MENU")),
            CreateScene(1000, 700, None), home,
            BagScene(1000, 700, None, items, home),
            AlchemyScene(1000, 700, None, items, player_provider=lambda: home.player),
            ShopScene(1000, 700, None, items, lambda: home.player),
            BattleScene(1000, 700, None, items, lambda: home.player, assets.get_background),
            StatusScene(1000, 700, None, lambda: home.player, home.level_system),
            SettingsScene(1000, 700, None, SettingsSystem(pathlib.Path(tempfile.gettempdir()) / "ui-settings.json"), GameSettings()),
        ]
        keys = ("MENU", "CREATE", "HOME", "BAG", "ALCHEMY", "SHOP", "BATTLE", "STATUS", "SETTINGS")
        for scene, key in zip(scenes, keys):
            if key != "MENU": scene.set_background(assets.get_background(key), 120)
        return scenes

    def test_14_menu_renders_with_background(self):
        scene = self._make_scenes()[0]; scene.draw(pygame.Surface((1000, 700)))

    def test_15_create_renders_input_panel(self):
        scene = self._make_scenes()[1]; scene.draw(pygame.Surface((1000, 700)))

    def test_16_home_renders_info_and_log_panels(self):
        scene = self._make_scenes()[2]; scene.draw(pygame.Surface((1000, 700)))

    def test_17_bag_and_alchemy_render_long_messages(self):
        scenes = self._make_scenes(); screen = pygame.Surface((1000, 700))
        for scene in scenes[3:5]: scene.message = "測試長訊息" * 30; scene.draw(screen)

    def test_18_shop_renders_long_transaction_message(self):
        scene = self._make_scenes()[5]; scene.message = "交易結果訊息" * 30; scene.draw(pygame.Surface((1000, 700)))

    def test_19_battle_renders_long_combat_message(self):
        scene = self._make_scenes()[6]; scene.enter(); scene.message = "戰鬥結果訊息" * 60; scene.draw(pygame.Surface((1000, 700)))

    def test_20_status_settings_and_debug_render(self):
        scenes = self._make_scenes(); screen = pygame.Surface((1000, 700))
        scenes[7].draw(screen); scenes[8].draw(screen)
        state = Mock(enabled=True, last_message="X" * 500)
        DebugOverlay(None, Mock(build_lines=lambda *args: ("X" * 500,))).draw(screen, state, "HOME", None, 60)


if __name__ == "__main__":
    unittest.main()

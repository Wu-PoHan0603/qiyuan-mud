import json
import pathlib
import tempfile
import time
import unittest
from unittest.mock import patch

import pygame

import release_check
from Main import HEIGHT, WIDTH
from Objects.GameSettings import GameSettings
from Objects.Player import Player
from SceneManager import SceneManager
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
from Systems.Save_system import SaveSystem
from Systems.asset_manager import AssetManager
from Systems.audio_manager import AudioManager
from Systems.error_logger import ErrorLogger
from Systems.settings_system import SettingsSystem


PROJECT_DIR = pathlib.Path(__file__).resolve().parents[1]


class ReleaseReadinessTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init(); pygame.display.set_mode((1, 1))

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    def test_01_release_check_all_passes(self):
        failed = [result for result in release_check.check_release(PROJECT_DIR) if not result[1]]
        self.assertEqual(failed, [])

    def test_02_runtime_dimensions_are_supported(self):
        self.assertGreaterEqual(WIDTH, 1000); self.assertGreaterEqual(HEIGHT, 700)

    def test_03_required_directories_exist(self):
        for name in ("Assets", "Font", "Objects", "Scenes", "Systems", "Ui", "data", "saves"):
            self.assertTrue((PROJECT_DIR / name).is_dir())

    def test_04_entrypoints_exist(self):
        for name in ("Main.py", "dev_runner.py", "release_check.py", "start_game.bat", "start_dev.bat"):
            self.assertTrue((PROJECT_DIR / name).is_file())

    def test_05_font_decodes(self):
        path = next((PROJECT_DIR / "Font").glob("*.ttf"))
        self.assertIsInstance(pygame.font.Font(str(path), 20), pygame.font.Font)

    def test_06_static_json_objects_are_nonempty(self):
        for path in (PROJECT_DIR / "data").glob("*.json"):
            self.assertTrue(json.loads(path.read_text(encoding="utf-8-sig")))

    def test_07_generated_asset_counts_match_release(self):
        backgrounds = [p for p in (PROJECT_DIR / "Assets/Background").glob("*.png") if p.name != "Background.png"]
        audio = list((PROJECT_DIR / "Assets/Audio").glob("*.wav"))
        self.assertEqual((len(backgrounds), len(audio)), (10, 5))

    def test_08_scene_registration_is_complete(self):
        expected = {"MENU", "CREATE", "HOME", "ALCHEMY", "BAG", "SHOP", "BATTLE", "STATUS", "SETTINGS"}
        manager = SceneManager()
        for name in expected: manager.add_scene(name, object())
        self.assertEqual(set(manager.scenes), expected)

    def test_09_legacy_save_loads_without_rewrite(self):
        with tempfile.TemporaryDirectory() as directory:
            legacy = pathlib.Path(directory) / "legacy.json"
            legacy.write_text((PROJECT_DIR / "save_data.json").read_text(encoding="utf-8-sig"), encoding="utf-8")
            system = SaveSystem(); system.save_file = str(pathlib.Path(directory) / "missing.json"); system.legacy_save_file = str(legacy)
            before = legacy.read_bytes(); self.assertIsInstance(system.load_game(), Player)
            self.assertEqual(legacy.read_bytes(), before)

    def test_10_formal_save_round_trip_preserves_player(self):
        with tempfile.TemporaryDirectory() as directory:
            system = SaveSystem(); system.save_file = str(pathlib.Path(directory) / "save.json"); system.legacy_save_file = str(pathlib.Path(directory) / "legacy.json")
            player = Player("發布測試", spiritual_root="金", inventory={"spirit_stone": 333, "iron_sword": 1})
            self.assertTrue(system.save_game(player)); self.assertEqual(system.load_game().to_dict(), player.to_dict())

    def test_11_settings_failed_replace_cleans_temp(self):
        with tempfile.TemporaryDirectory() as directory:
            path = pathlib.Path(directory) / "settings.json"; system = SettingsSystem(path)
            with patch("pathlib.Path.replace", side_effect=OSError("busy")):
                self.assertFalse(system.save(GameSettings()))
            self.assertFalse(path.with_suffix(".json.tmp").exists()); self.assertIn("busy", system.last_error)

    def test_12_error_logger_writes_traceback(self):
        with tempfile.TemporaryDirectory() as directory:
            logger = ErrorLogger(directory)
            try: raise RuntimeError("release-test")
            except RuntimeError as error:
                self.assertTrue(logger.log_exception(type(error), error, error.__traceback__))
            self.assertIn("release-test", logger.log_file.read_text(encoding="utf-8"))

    def test_13_error_logger_failure_is_nonfatal(self):
        logger = ErrorLogger(PROJECT_DIR)
        with patch("pathlib.Path.mkdir", side_effect=OSError("readonly")):
            self.assertFalse(logger.log_exception(RuntimeError, RuntimeError("x"), None))

    def test_14_windows_launchers_use_project_directory(self):
        for name in ("start_game.bat", "start_dev.bat"):
            text = (PROJECT_DIR / name).read_text(encoding="utf-8")
            self.assertIn('cd /d "%~dp0"', text)

    def test_15_mvp_player_flow_round_trip(self):
        with tempfile.TemporaryDirectory() as directory:
            items = ItemSystem(); home = HomeScene(1000, 700, None, item_system=items)
            created = Player("流程測試", spiritual_root="火", inventory={"spirit_stone": 1000, "spirit_grass": 100})
            home.set_player(created); home._train(); home.player.mp = 50; home._meditate(); home._explore()
            shop = ShopScene(1000, 700, None, items, lambda: home.player); shop.handle_event(pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=shop.btn_buy.rect.center))
            alchemy = AlchemyScene(1000, 700, None, items, player_provider=lambda: home.player); alchemy.refine()
            system = SaveSystem(); system.save_file = str(pathlib.Path(directory) / "save.json"); system.legacy_save_file = str(pathlib.Path(directory) / "legacy.json")
            self.assertTrue(system.save_game(home.prepare_player_for_save())); self.assertEqual(system.load_game().name, "流程測試")

    def test_16_background_load_benchmark(self):
        start = time.perf_counter(); manager = AssetManager(PROJECT_DIR, (1000, 700)); self.assertTrue(manager.load_all()[0])
        self.assertLess(time.perf_counter() - start, 8.0)

    def test_17_scene_draw_benchmark(self):
        assets = AssetManager(PROJECT_DIR, (1000, 700)); assets.load_all(); items = ItemSystem(); home = HomeScene(1000, 700, None, item_system=items); items.load_save_data(home.player.inventory)
        scenes = [MenuScene(1000,700,None,assets.get_background("MENU")), CreateScene(1000,700,None), home, BagScene(1000,700,None,items,home), AlchemyScene(1000,700,None,items,player_provider=lambda:home.player), ShopScene(1000,700,None,items,lambda:home.player), BattleScene(1000,700,None,items,lambda:home.player,assets.get_background), StatusScene(1000,700,None,lambda:home.player,home.level_system), SettingsScene(1000,700,None,SettingsSystem(pathlib.Path(tempfile.gettempdir())/"release-settings.json"),GameSettings())]
        screen = pygame.Surface((1000,700)); start=time.perf_counter()
        for scene in scenes: scene.draw(screen)
        self.assertLess(time.perf_counter()-start, 2.0)

    def test_18_gitignore_covers_runtime_files(self):
        text = (PROJECT_DIR / ".gitignore").read_text(encoding="utf-8")
        for entry in ("__pycache__/", "logs/", "saves/*.tmp", "saves/debug_save.json"):
            self.assertIn(entry, text)

    def test_19_readme_documents_run_and_test(self):
        text = (PROJECT_DIR / "README.md").read_text(encoding="utf-8")
        self.assertIn("python Main.py", text); self.assertIn("release_check.py", text); self.assertIn("unittest", text)

    def test_20_audio_and_assets_survive_reload(self):
        assets = AssetManager(PROJECT_DIR,(1000,700)); assets.load_all(); self.assertTrue(assets.reload_all()[0])
        audio = AudioManager(PROJECT_DIR); audio.current_key=None; self.assertTrue(audio.reload()[0])


if __name__ == "__main__":
    unittest.main()

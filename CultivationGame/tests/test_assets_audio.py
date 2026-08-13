import pathlib
import tempfile
import unittest
from unittest.mock import Mock, patch

import pygame

from Objects.GameSettings import GameSettings
from Objects.Player import Player
from SceneManager import SceneManager
from Scenes.BaseScene import BaseScene
from Scenes.Battle import BattleScene
from Scenes.Home import HomeScene
from Scenes.Settings import SettingsScene
from Systems.Item_system import ItemSystem
from Systems.asset_manager import AssetManager
from Systems.audio_manager import AudioManager
from Systems.meditation_system import MeditationSystem
from Systems.settings_system import SettingsSystem


PROJECT_DIR = pathlib.Path(__file__).resolve().parents[1]


class AssetAudioTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()
        pygame.display.set_mode((1, 1))

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    def test_01_background_manifest_covers_registered_scenes(self):
        required = {"MENU", "CREATE", "HOME", "ALCHEMY", "BAG", "SHOP", "BATTLE", "STATUS", "SETTINGS"}
        self.assertTrue(required.issubset(AssetManager.BACKGROUNDS))

    def test_02_all_background_files_exist(self):
        manager = AssetManager(PROJECT_DIR, (1000, 700))
        for filename in set(manager.BACKGROUNDS.values()):
            self.assertTrue((manager.asset_dir / filename).is_file())

    def test_03_all_backgrounds_decode_and_scale(self):
        manager = AssetManager(PROJECT_DIR, (1000, 700))
        ok, _ = manager.load_all()
        self.assertTrue(ok)
        self.assertTrue(all(image.get_size() == (1000, 700) for image in manager.backgrounds.values()))

    def test_04_missing_background_uses_fallback(self):
        with tempfile.TemporaryDirectory() as directory:
            manager = AssetManager(directory, (320, 180))
            ok, _ = manager.load_all()
            self.assertFalse(ok)
            self.assertEqual(manager.get_background("HOME").get_size(), (320, 180))

    def test_05_corrupt_reload_preserves_previous_backgrounds(self):
        manager = AssetManager(PROJECT_DIR, (320, 180))
        self.assertTrue(manager.load_all()[0])
        original = manager.backgrounds
        with patch.object(manager, "_load_image", side_effect=pygame.error("broken")):
            self.assertFalse(manager.reload_all()[0])
        self.assertIs(manager.backgrounds, original)

    def test_06_unknown_background_key_returns_fallback(self):
        manager = AssetManager(PROJECT_DIR, (123, 77))
        self.assertEqual(manager.get_background("UNKNOWN").get_size(), (123, 77))

    def test_07_base_scene_draws_background_and_shade(self):
        scene = BaseScene()
        background = pygame.Surface((20, 20)); background.fill((200, 200, 200))
        scene.set_background(background, 100)
        screen = pygame.Surface((20, 20))
        scene.draw_background(screen)
        self.assertLess(screen.get_at((10, 10)).r, 200)

    def test_08_base_scene_without_background_draws_fallback(self):
        scene = BaseScene(); screen = pygame.Surface((20, 20))
        scene.draw_background(screen, (1, 2, 3))
        self.assertEqual(screen.get_at((0, 0))[:3], (1, 2, 3))

    def test_09_audio_manifest_contains_five_requested_tracks(self):
        expected = {"background_theme.wav", "battle_theme.wav", "cultivator_home_theme.wav", "meditation_theme.wav", "shop_theme.wav"}
        self.assertEqual(set(AudioManager.TRACKS.values()), expected)

    def test_10_all_audio_files_validate(self):
        manager = AudioManager(PROJECT_DIR)
        self.assertTrue(manager.validate_all()[0])

    def test_11_missing_audio_is_reported_without_exception(self):
        manager = AudioManager(pathlib.Path(tempfile.gettempdir()) / "not-a-project")
        self.assertFalse(manager.validate_all()[0])

    def test_12_no_mixer_device_degrades_safely(self):
        manager = AudioManager(PROJECT_DIR)
        manager.enabled = False
        ok, message = manager.play_scene("HOME")
        self.assertFalse(ok)
        self.assertIn("靜音", message)

    def test_13_unknown_scene_audio_is_rejected(self):
        manager = AudioManager(PROJECT_DIR)
        self.assertFalse(manager.play_scene("UNKNOWN")[0])

    def test_14_volume_is_clamped(self):
        manager = AudioManager(PROJECT_DIR)
        manager.enabled = False
        manager.set_volume(150); self.assertEqual(manager.volume, 100)
        manager.set_volume(-1); self.assertEqual(manager.volume, 0)

    def test_15_scene_manager_notifies_audio_after_change(self):
        audio = Mock()
        manager = SceneManager(audio)
        manager.add_scene("HOME", BaseScene())
        manager.change_scene("HOME")
        audio.play_scene.assert_called_once_with("HOME")

    def test_16_scene_reload_does_not_create_duplicate_manager_state(self):
        audio = Mock()
        manager = SceneManager(audio)
        scene = BaseScene(); manager.add_scene("HOME", scene)
        manager.change_scene("HOME"); manager.reload_current()
        self.assertIs(manager.current, scene)
        self.assertEqual(audio.play_scene.call_count, 2)

    def test_17_home_meditation_requests_meditation_music(self):
        audio = Mock()
        home = HomeScene(1000, 700, None, item_system=ItemSystem(), meditation_system=MeditationSystem(lambda a, b: 20), audio_manager=audio)
        home.player.mp = 50
        home._meditate()
        audio.play_scene.assert_called_once_with("MEDITATE")

    def test_18_settings_volume_updates_audio_manager(self):
        with tempfile.TemporaryDirectory() as directory:
            audio = Mock()
            settings = GameSettings(master_volume=25)
            scene = SettingsScene(1000, 700, None, SettingsSystem(pathlib.Path(directory) / "settings.json"), settings, audio)
            scene._save_current("saved")
            audio.set_volume.assert_called_once_with(25)

    def test_19_high_realm_battle_uses_demon_background(self):
        player = Player(realm="化神期第1層", realm_index=4)
        requested = []
        provider = lambda key: requested.append(key) or pygame.Surface((1000, 700))
        battle = BattleScene(1000, 700, None, ItemSystem(), lambda: player, provider)
        battle.enter()
        self.assertEqual(requested[-1], "BATTLE_DEMON")

    def test_20_asset_and_audio_reload_succeeds(self):
        assets = AssetManager(PROJECT_DIR, (1000, 700))
        assets.load_all()
        self.assertTrue(assets.reload_all()[0])
        audio = AudioManager(PROJECT_DIR)
        audio.current_key = None
        self.assertTrue(audio.reload()[0])


if __name__ == "__main__":
    unittest.main()

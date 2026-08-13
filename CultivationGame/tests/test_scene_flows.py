import pathlib
import tempfile
import unittest

import pygame

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
from Systems.alchemy_system import AlchemySystem
from Systems.exploration_system import ExplorationSystem
from Systems.meditation_system import MeditationSystem
from Systems.settings_system import SettingsSystem
from Ui.Button import Button


def click(target):
    return pygame.event.Event(
        pygame.MOUSEBUTTONDOWN,
        button=1,
        pos=target.rect.center,
    )


class SceneFlowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()
        pygame.display.set_mode((1, 1))

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    def make_home(self, **systems):
        items = ItemSystem()
        home = HomeScene(1000, 700, None, item_system=items, **systems)
        items.load_save_data(home.player.inventory)
        return home, items

    def test_01_button_requires_one_left_click_event(self):
        button = Button(10, 10, 100, 40, "Test")
        self.assertTrue(button.is_clicked(click(button)))
        held = pygame.event.Event(pygame.MOUSEMOTION, pos=button.rect.center)
        right = pygame.event.Event(
            pygame.MOUSEBUTTONDOWN, button=3, pos=button.rect.center
        )
        self.assertFalse(button.is_clicked(held))
        self.assertFalse(button.is_clicked(right))

    def test_02_scene_manager_only_dispatches_current_scene(self):
        class Spy:
            def __init__(self, result):
                self.result = result
                self.events = 0
                self.updates = 0

            def handle_event(self, event):
                self.events += 1
                return self.result

            def update(self):
                self.updates += 1

        first, second = Spy("FIRST"), Spy("SECOND")
        manager = SceneManager()
        manager.add_scene("A", first)
        manager.add_scene("B", second)
        manager.change_scene("A")
        self.assertEqual(manager.handle_event(object()), "FIRST")
        manager.change_scene("B")
        manager.update()
        self.assertEqual((first.events, first.updates), (1, 0))
        self.assertEqual((second.events, second.updates), (0, 1))

    def test_03_menu_routes_start_load_and_quit(self):
        menu = MenuScene(1000, 700, None, pygame.Surface((1000, 700)))
        expected = ("CREATE", "LOAD", "QUIT")
        for button, result in zip(menu.buttons, expected):
            self.assertEqual(menu.handle_event(click(button)), result)

    def test_04_create_confirmation_builds_valid_player(self):
        scene = CreateScene(1000, 700, None)
        scene.player_name = "青雲"
        self.assertEqual(scene.handle_event(click(scene.btn_confirm)), "HOME")
        self.assertIsInstance(scene.created_player, Player)
        self.assertEqual(scene.created_player.name, "青雲")
        self.assertEqual(scene.created_player.spirit_stone, 100)

    def test_05_create_name_input_respects_eight_character_limit(self):
        scene = CreateScene(1000, 700, None)
        scene.input_active = True
        scene.player_name = "一二三四五六七八"
        scene.handle_event(pygame.event.Event(pygame.TEXTINPUT, text="九"))
        self.assertEqual(scene.player_name, "一二三四五六七八")

    def test_06_archive_routes_to_each_scene_once(self):
        home, _ = self.make_home()
        for action, expected in (
            ("STATUS", "STATUS"), ("BAG", "BAG"),
            ("ALCHEMY", "ALCHEMY"), ("SHOP", "SHOP"),
            ("BOSS", "BATTLE"), ("SETTING", "SETTINGS"),
        ):
            home.archive_menu.open()
            button = home.archive_menu.buttons[action]
            self.assertEqual(home.handle_event(click(button)), expected)
            self.assertFalse(home.archive_menu.is_open)

    def test_07_home_training_changes_cultivation(self):
        home, _ = self.make_home()
        before = home.player.cultivation
        home.handle_event(click(home.btn_train))
        self.assertGreater(home.player.cultivation, before)

    def test_08_home_meditation_caps_mp(self):
        home, _ = self.make_home(
            meditation_system=MeditationSystem(lambda low, high: 50)
        )
        home.player.mp = 80
        home.archive_menu.open()
        home.handle_event(click(home.archive_menu.buttons["MEDITATE"]))
        self.assertEqual(home.player.mp, home.player.max_mp)

    def test_09_home_exploration_updates_resources(self):
        exploration = ExplorationSystem(
            choice=lambda events: "發現靈石礦脈",
            randint=lambda low, high: 40,
        )
        home, items = self.make_home(exploration_system=exploration)
        before = items.get_item_count("spirit_stone")
        home.archive_menu.open()
        home.handle_event(click(home.archive_menu.buttons["EXPLORE"]))
        self.assertEqual(items.get_item_count("spirit_stone"), before + 40)

    def test_10_empty_bag_updates_and_draws_without_crash(self):
        home, items = self.make_home()
        items.load_save_data({item_id: 0 for item_id in items.item_database})
        bag = BagScene(1000, 700, None, items, home)
        bag.update()
        bag.draw(pygame.Surface((1000, 700)))

    def test_11_bag_equips_selected_weapon(self):
        home, items = self.make_home()
        items.add_item("iron_sword")
        bag = BagScene(1000, 700, None, items, home)
        bag.selected_item = "iron_sword"
        bag.handle_event(click(bag.btn_use_gathering))
        self.assertEqual((home.player.weapon, home.player.weapon_atk), ("鐵劍", 25))

    def test_12_bag_equips_selected_armor(self):
        home, items = self.make_home()
        items.add_item("iron_armor")
        bag = BagScene(1000, 700, None, items, home)
        bag.selected_item = "iron_armor"
        bag.handle_event(click(bag.btn_use_gathering))
        self.assertEqual((home.player.armor, home.player.armor_def), ("鐵衣", 20))

    def test_13_missing_consumable_never_becomes_negative(self):
        home, items = self.make_home()
        bag = BagScene(1000, 700, None, items, home)
        bag.selected_item = "gathering_pill"
        bag.handle_event(click(bag.btn_use_gathering))
        self.assertEqual(items.get_item_count("gathering_pill"), 0)

    def test_14_shop_one_click_makes_one_purchase(self):
        home, items = self.make_home()
        shop = ShopScene(1000, 700, None, items, lambda: home.player)
        before_stones = items.get_item_count("spirit_stone")
        before_items = items.get_item_count("gathering_pill")
        shop.handle_event(click(shop.btn_buy))
        self.assertEqual(items.get_item_count("spirit_stone"), before_stones - 20)
        self.assertEqual(items.get_item_count("gathering_pill"), before_items + 1)

    def test_15_shop_insufficient_funds_changes_nothing(self):
        home, items = self.make_home()
        items.load_save_data({"spirit_stone": 0})
        shop = ShopScene(1000, 700, None, items, lambda: home.player)
        shop.handle_event(click(shop.btn_buy))
        self.assertEqual(items.get_item_count("spirit_stone"), 0)
        self.assertEqual(items.get_item_count("gathering_pill"), 0)

    def test_16_alchemy_one_click_consumes_one_recipe_cost(self):
        home, items = self.make_home()
        alchemy = AlchemyScene(
            1000, 700, None, items,
            AlchemySystem(randint=lambda low, high: 1),
            lambda: home.player,
        )
        before = items.get_item_count("spirit_stone")
        alchemy.handle_event(click(alchemy.btn_refine))
        self.assertEqual(items.get_item_count("spirit_stone"), before - 30)
        self.assertEqual(items.get_item_count("gathering_pill"), 1)

    def test_17_battle_attack_is_one_complete_turn(self):
        home, items = self.make_home()
        battle = BattleScene(1000, 700, None, items, lambda: home.player)
        boss_hp, player_hp = battle.boss.hp, home.player.hp
        battle.handle_event(click(battle.buttons["攻擊"]))
        self.assertLess(battle.boss.hp, boss_hp)
        self.assertLess(home.player.hp, player_hp)

    def test_18_battle_skill_with_low_mp_changes_nothing(self):
        home, items = self.make_home()
        home.player.mp = 0
        battle = BattleScene(1000, 700, None, items, lambda: home.player)
        boss_hp, player_hp = battle.boss.hp, home.player.hp
        battle.handle_event(click(battle.buttons["技能"]))
        self.assertEqual((battle.boss.hp, home.player.hp), (boss_hp, player_hp))
        self.assertEqual(home.player.mp, 0)

    def test_19_flee_then_reenter_starts_fresh_battle(self):
        home, items = self.make_home()
        battle = BattleScene(1000, 700, None, items, lambda: home.player)
        self.assertEqual(battle.handle_event(click(battle.buttons["逃跑"])), "HOME")
        self.assertTrue(battle.system.battle_finished)
        battle.enter()
        self.assertFalse(battle.system.battle_finished)
        self.assertEqual(battle.boss.hp, battle.boss.max_hp)

    def test_20_all_scenes_smoke_and_save_round_trip(self):
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            save = SaveSystem()
            save.save_file = str(root / "save.json")
            save.legacy_save_file = str(root / "legacy.json")
            items = ItemSystem()
            home = HomeScene(1000, 700, None, save, items)
            items.load_save_data(home.player.inventory)
            settings_system = SettingsSystem(root / "settings.json")
            scenes = {
                "MENU": MenuScene(1000, 700, None, pygame.Surface((1000, 700))),
                "CREATE": CreateScene(1000, 700, None),
                "HOME": home,
                "BAG": BagScene(1000, 700, None, items, home),
                "ALCHEMY": AlchemyScene(1000, 700, None, items, player_provider=lambda: home.player),
                "SHOP": ShopScene(1000, 700, None, items, lambda: home.player),
                "BATTLE": BattleScene(1000, 700, None, items, lambda: home.player),
                "STATUS": StatusScene(1000, 700, None, lambda: home.player, home.level_system),
                "SETTINGS": SettingsScene(1000, 700, None, settings_system, GameSettings()),
            }
            manager = SceneManager()
            screen = pygame.Surface((1000, 700))
            for name, scene in scenes.items():
                manager.add_scene(name, scene)
                manager.change_scene(name)
                manager.update()
                manager.draw(screen)
            self.assertTrue(save.save_game(home.prepare_player_for_save()))
            self.assertEqual(save.load_game().to_dict(), home.player.to_dict())


if __name__ == "__main__":
    unittest.main()

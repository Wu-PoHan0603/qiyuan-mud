import json
import pathlib
import tempfile
import unittest

import dev_runner
from Objects.DebugState import DebugState
from Objects.Player import Player
from Objects.GameSettings import GameSettings
from Systems.Battle_system import BattleSystem
from Systems.Item_system import ItemSystem
from Systems.Level_system import LevelSystem
from Systems.Reward_system import RewardSystem
from Systems.Save_system import SaveSystem
from Systems.alchemy_system import AlchemySystem
from Systems.cultivation_system import CultivationSystem
from Systems.exploration_system import ExplorationSystem
from Systems.experience_system import ExperienceSystem
from Systems.fast_training_system import FastTrainingSystem
from Systems.meditation_system import MeditationSystem
from Systems.shop_system import ShopSystem
from Systems.data_loader import load_bosses, load_items, load_skills
from Systems.data_reload_system import DataReloadSystem
from Systems.debug_system import DebugSystem
from Systems.settings_system import SettingsSystem


class CoreMvpTests(unittest.TestCase):
    def test_player_defaults_and_validation(self):
        player = Player()
        self.assertEqual((player.hp, player.max_hp), (100, 100))
        self.assertEqual((player.mp, player.max_mp), (100, 100))
        self.assertEqual(player.realm_index, 0)
        data = player.to_dict()
        data["hp"] = -1
        with self.assertRaises(ValueError):
            Player.from_dict(data)

    def test_nine_realms_and_cap(self):
        system = LevelSystem()
        self.assertEqual(len(system.realms), 82)
        qi_nine = system.realms[9]
        result = system.add_cultivation(
            qi_nine["name"], qi_nine["max_cultivation"] - 1, 100
        )
        self.assertEqual(
            result[:2], (qi_nine["name"], qi_nine["max_cultivation"])
        )
        highest = system.realms[-1]
        result = system.add_cultivation(
            highest["name"], highest["max_cultivation"] - 1, 999999999
        )
        self.assertEqual(
            result[:2], (highest["name"], highest["max_cultivation"])
        )

    def test_cultivation_and_meditation(self):
        values = iter((91, 120))
        player = Player()
        ok, _ = CultivationSystem(
            lambda low, high: next(values)
        ).cultivate(player, LevelSystem())
        self.assertTrue(ok)
        self.assertNotEqual(player.realm, "凡人境界")
        player.mp = 90
        ok, amount, _ = MeditationSystem(
            lambda low, high: 50
        ).meditate(player)
        self.assertTrue(ok)
        self.assertEqual((amount, player.mp), (10, 100))

    def test_exploration_boundaries(self):
        player = Player(hp=5)
        items = ItemSystem()
        system = ExplorationSystem(
            lambda events: "遭遇妖獸", lambda low, high: 30
        )
        ok, _ = system.explore(player, items, LevelSystem())
        self.assertTrue(ok)
        self.assertEqual(player.hp, 0)

    def test_experience_and_exploration_level_up(self):
        player = Player()
        system = ExperienceSystem()
        self.assertTrue(system.add_exp(player, 99)[0])
        self.assertEqual((player.level, player.exp), (1, 99))
        items = ItemSystem()
        explore = ExplorationSystem(
            lambda events: events[0],
            lambda low, high: low,
            system,
        )
        self.assertTrue(explore.explore(player, items, LevelSystem())[0])
        self.assertEqual((player.level, player.exp), (2, 99))

    def test_alchemy_cost_and_rate(self):
        items = ItemSystem()
        ok, _ = AlchemySystem(
            lambda low, high: 60
        ).refine(items, "gathering_pill")
        self.assertTrue(ok)
        self.assertEqual(items.get_item_count("spirit_stone"), 70)
        self.assertEqual(items.get_item_count("gathering_pill"), 1)

    def test_shop_and_skill_switch(self):
        player = Player()
        items = ItemSystem()
        items.inventory["spirit_stone"] = 1000
        self.assertTrue(
            ShopSystem().buy(player, items, "ice_arrow_scroll")[0]
        )
        self.assertTrue(
            items.use_or_equip(
                player, "ice_arrow_scroll", LevelSystem()
            )[0]
        )
        self.assertEqual((player.skill, player.skill_power), ("冰箭術", 80))
        self.assertGreaterEqual(player.spirit_stone, 0)

    def test_boss_reward_only_once(self):
        player = Player(weapon="玄鐵劍", weapon_atk=100)
        items = ItemSystem()
        system = BattleSystem(
            RewardSystem(lambda drops: "gathering_pill")
        )
        boss = system.create_boss()
        self.assertTrue(system.attack(player, boss)[0])
        self.assertTrue(boss.is_dead)
        self.assertEqual(player.hp, player.max_hp)
        self.assertTrue(system.claim_reward(player, boss, items)[0])
        self.assertFalse(system.claim_reward(player, boss, items)[0])
        self.assertEqual((player.level, player.exp), (2, 0))

    def test_versioned_save_and_legacy_load(self):
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            system = SaveSystem()
            system.save_file = str(root / "saves" / "save.json")
            system.legacy_save_file = str(root / "save_data.json")
            self.assertTrue(system.save_game(Player()))
            payload = json.loads(
                pathlib.Path(system.save_file).read_text(encoding="utf-8")
            )
            self.assertEqual(payload["save_version"], 1)
            self.assertIsInstance(system.load_game(), Player)
            pathlib.Path(system.save_file).unlink()
            pathlib.Path(system.legacy_save_file).write_text(
                json.dumps(Player().to_dict(), ensure_ascii=False),
                encoding="utf-8",
            )
            self.assertIsInstance(system.load_game(), Player)

    def test_all_major_breakthrough_pills(self):
        level_system = LevelSystem()
        self.assertEqual(len(level_system.BREAKTHROUGH_PILLS), 8)
        for realm, (pill_id, _, next_realm) in (
            level_system.BREAKTHROUGH_PILLS.items()
        ):
            player = Player()
            player.realm = realm
            player.realm_index = player._get_realm_index(realm)
            player.cultivation = level_system.get_max_cultivation(realm)
            items = ItemSystem()
            self.assertFalse(
                level_system.attempt_major_breakthrough(player, items)[1]
            )
            items.inventory[pill_id] = 1
            self.assertTrue(
                level_system.attempt_major_breakthrough(player, items)[1]
            )
            self.assertEqual(player.realm, next_realm)
            self.assertEqual(items.get_item_count(pill_id), 0)

    def test_static_game_data(self):
        self.assertEqual(len(load_items()), 23)
        self.assertEqual(len(load_bosses()), 9)
        self.assertIn("qi_wolf", load_bosses())
        self.assertEqual(len(load_skills()), 4)
        self.assertEqual(len(AlchemySystem.RECIPES), 9)

    def test_nine_realm_boss_progression(self):
        bosses = load_bosses()
        expected_pills = [
            value[0]
            for value in LevelSystem.BREAKTHROUGH_PILLS.values()
        ]
        for realm_index in range(9):
            system = BattleSystem(
                RewardSystem(lambda drops: drops[0])
            )
            player = Player(
                realm_index=realm_index,
                weapon_atk=10000,
                armor_def=10000,
            )
            items = ItemSystem()
            grass_before = items.get_item_count("spirit_grass")
            boss = system.create_boss_for_player(player)
            boss_data = next(
                data
                for data in bosses.values()
                if data["realm_index"] == realm_index
            )
            self.assertEqual(boss.name, boss_data["name"])
            self.assertTrue(system.attack(player, boss)[0])
            self.assertTrue(boss.is_dead)
            self.assertTrue(
                system.claim_reward(player, boss, items)[0]
            )
            self.assertEqual(
                items.get_item_count("spirit_grass"),
                grass_before + boss_data["spirit_grass"],
            )
            if realm_index < 8:
                self.assertEqual(
                    items.get_item_count(expected_pills[realm_index]),
                    1,
                )

    def test_combat_scaling_and_defeat_recovery(self):
        system = BattleSystem()
        skill_name = next(iter(system.skills))
        skill = system.skills[skill_name]
        player = Player(
            level=10,
            skill=skill_name,
            skill_power=skill["power"],
            mp=100,
            armor_def=5,
        )
        boss = system.create_boss()
        hp_before = boss.hp
        self.assertTrue(system.use_skill(player, boss)[0])
        self.assertEqual(
            boss.hp,
            max(0, hp_before - skill["power"] - 27),
        )
        player.hp = 0
        player.mp = 0
        self.assertTrue(system.recover_after_defeat(player)[0])
        self.assertEqual(player.hp, player.max_hp // 2)
        self.assertEqual(player.mp, player.max_mp // 4)

    def test_fast_training_stops_at_major_bottleneck(self):
        level_system = LevelSystem()
        player = Player()
        player.realm = level_system.realms[9]["name"]
        player.realm_index = player._get_realm_index(player.realm)
        player.cultivation = level_system.realms[9]["max_cultivation"]
        state = (player.realm, player.cultivation)
        ok, _ = FastTrainingSystem().train(
            player,
            level_system,
            CultivationSystem(lambda low, high: low),
        )
        self.assertFalse(ok)
        self.assertEqual((player.realm, player.cultivation), state)

    def test_settings_round_trip_and_corruption_fallback(self):
        with tempfile.TemporaryDirectory() as directory:
            path = pathlib.Path(directory) / "settings.json"
            system = SettingsSystem(path)
            settings = GameSettings(120, 25, True)
            self.assertTrue(system.save(settings))
            self.assertEqual(system.load().to_dict(), settings.to_dict())
            path.write_text("{broken", encoding="utf-8")
            self.assertEqual(
                system.load().to_dict(),
                GameSettings().to_dict(),
            )
            self.assertIsNotNone(system.last_error)

    def test_atomic_data_reload_preserves_inventory(self):
        reload_system = DataReloadSystem()
        ok, bundle, _ = reload_system.validate_all()
        self.assertTrue(ok)
        items = ItemSystem()
        items.inventory["gathering_pill"] = 7
        alchemy = AlchemySystem()
        battle = BattleSystem()
        self.assertTrue(
            reload_system.apply_all(
                bundle,
                items,
                alchemy,
                battle,
            )[0]
        )
        self.assertEqual(items.get_item_count("gathering_pill"), 7)
        invalid = dict(bundle)
        invalid["items"] = dict(bundle["items"])
        invalid["items"].pop("gathering_pill")
        snapshot = items.item_database
        self.assertFalse(
            reload_system.apply_all(
                invalid,
                items,
                alchemy,
                battle,
            )[0]
        )
        self.assertIs(items.item_database, snapshot)

    def test_debug_state_and_diagnostics(self):
        state = DebugState()
        system = DebugSystem()
        self.assertFalse(state.enabled)
        self.assertTrue(system.toggle(state))
        lines = system.build_lines(state, "HOME", Player("Tester"), 60)
        self.assertIn("Scene: HOME", lines)
        self.assertIn("Player: Tester", lines)

    def test_debug_save_is_isolated_from_normal_save(self):
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            system = SaveSystem()
            system.save_file = str(root / "save.json")
            system.debug_save_file = str(root / "debug_save.json")
            system.legacy_save_file = str(root / "legacy.json")
            self.assertTrue(system.save_game(Player("Normal")))
            normal_data = pathlib.Path(system.save_file).read_bytes()
            self.assertTrue(system.save_debug_game(Player("Debug")))
            self.assertEqual(
                pathlib.Path(system.save_file).read_bytes(), normal_data
            )
            self.assertEqual(system.load_game().name, "Normal")
            self.assertEqual(system.load_debug_game().name, "Debug")

    def test_dev_runner_detects_and_rejects_invalid_python(self):
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            source = root / "sample.py"
            source.write_text("value = 1\n", encoding="utf-8")
            before = dev_runner.snapshot_python_files(root)
            source.write_text("if:\n", encoding="utf-8")
            after = dev_runner.snapshot_python_files(root)
            self.assertEqual(
                dev_runner.changed_files(before, after), [source]
            )
            valid, errors = dev_runner.validate_python_files(root)
            self.assertFalse(valid)
            self.assertTrue(errors)


if __name__ == "__main__":
    unittest.main()

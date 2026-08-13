import json
import os
import pathlib
import tempfile
import unittest
from unittest.mock import patch

from Objects.Player import Player
from Systems.Save_system import SaveSystem


class SaveSecurityTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self.temporary.name)
        self.system = SaveSystem()
        self.system.save_file = str(self.root / "save.json")
        self.system.debug_save_file = str(self.root / "debug_save.json")
        self.system.legacy_save_file = str(self.root / "legacy.json")

    def tearDown(self):
        self.temporary.cleanup()

    def write_raw(self, text, path=None):
        target = pathlib.Path(path or self.system.save_file)
        target.write_text(text, encoding="utf-8")

    def write_player_data(self, mutate=None, path=None):
        player_data = Player("安全測試").to_dict()
        if mutate is not None:
            mutate(player_data)
        payload = {"save_version": 1, "player": player_data}
        self.write_raw(json.dumps(payload, ensure_ascii=False), path)

    def test_01_missing_save_returns_none(self):
        self.assertIsNone(self.system.load_game())
        self.assertFalse(self.system.has_save())

    def test_02_blank_save_is_rejected(self):
        self.write_raw("")
        self.assertIsNone(self.system.load_game())

    def test_03_malformed_json_is_rejected(self):
        self.write_raw('{"save_version": 1,')
        self.assertIsNone(self.system.load_game())

    def test_04_non_object_json_is_rejected(self):
        self.write_raw("[]")
        self.assertIsNone(self.system.load_game())

    def test_05_unsupported_save_version_is_rejected(self):
        self.write_raw(json.dumps({"save_version": 999, "player": {}}))
        self.assertIsNone(self.system.load_game())

    def test_06_missing_player_object_is_rejected(self):
        self.write_raw(json.dumps({"save_version": 1}))
        self.assertIsNone(self.system.load_game())

    def test_07_invalid_player_name_is_rejected(self):
        self.write_player_data(lambda data: data.update(name=123))
        self.assertIsNone(self.system.load_game())
        self.write_player_data(lambda data: data.update(name="超過八個字的修仙者名稱"))
        self.assertIsNone(self.system.load_game())

    def test_08_unknown_spiritual_root_is_rejected(self):
        self.write_player_data(lambda data: data.update(spiritual_root="暗"))
        self.assertIsNone(self.system.load_game())

    def test_09_unknown_realm_is_rejected(self):
        self.write_player_data(lambda data: data.update(realm="仙帝期"))
        self.assertIsNone(self.system.load_game())

    def test_10_mismatched_realm_index_is_rejected(self):
        self.write_player_data(
            lambda data: data.update(realm="金丹期第1層", realm_index=0)
        )
        self.assertIsNone(self.system.load_game())

    def test_11_non_object_inventory_is_rejected(self):
        self.write_player_data(lambda data: data.update(inventory=[]))
        self.assertIsNone(self.system.load_game())

    def test_12_unknown_inventory_item_is_rejected(self):
        def add_unknown(data):
            data["inventory"]["admin_item"] = 1

        self.write_player_data(add_unknown)
        self.assertIsNone(self.system.load_game())

    def test_13_boolean_inventory_amount_is_rejected(self):
        def set_boolean(data):
            data["inventory"]["spirit_stone"] = True

        self.write_player_data(set_boolean)
        self.assertIsNone(self.system.load_game())

    def test_14_negative_inventory_amount_is_rejected(self):
        def set_negative(data):
            data["inventory"]["gathering_pill"] = -1

        self.write_player_data(set_negative)
        self.assertIsNone(self.system.load_game())

    def test_15_hp_outside_maximum_is_rejected(self):
        self.write_player_data(lambda data: data.update(hp=101, max_hp=100))
        self.assertIsNone(self.system.load_game())

    def test_16_mp_below_zero_is_rejected(self):
        self.write_player_data(lambda data: data.update(mp=-1))
        self.assertIsNone(self.system.load_game())

    def test_17_equipment_value_mismatch_is_rejected(self):
        self.write_player_data(
            lambda data: data.update(weapon="木劍", weapon_atk=9999)
        )
        self.assertIsNone(self.system.load_game())

    def test_18_corrupt_debug_save_never_falls_back_to_normal(self):
        self.assertTrue(self.system.save_game(Player("正式角色")))
        self.write_raw("{broken", self.system.debug_save_file)
        self.assertIsNone(self.system.load_debug_game())
        self.assertEqual(self.system.load_game().name, "正式角色")

    def test_19_failed_atomic_replace_keeps_old_save_and_removes_temp(self):
        self.assertTrue(self.system.save_game(Player("舊角色")))
        old_bytes = pathlib.Path(self.system.save_file).read_bytes()
        with patch("Systems.Save_system.os.replace", side_effect=OSError("busy")):
            self.assertFalse(self.system.save_game(Player("新角色")))
        self.assertEqual(pathlib.Path(self.system.save_file).read_bytes(), old_bytes)
        self.assertFalse(pathlib.Path(self.system.save_file + ".tmp").exists())

    def test_20_valid_unicode_save_round_trip_is_exact(self):
        player = Player(
            "青雲子",
            spiritual_root="水",
            realm="築基期第3層",
            realm_index=1,
            cultivation=321,
            hp=73,
            mp=42,
            inventory={"spirit_stone": 987, "gathering_pill": 4},
        )
        self.assertTrue(self.system.save_game(player))
        loaded = self.system.load_game()
        self.assertEqual(loaded.to_dict(), player.to_dict())


if __name__ == "__main__":
    unittest.main()

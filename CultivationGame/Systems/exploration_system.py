import random

from Objects.Player import Player
from Systems.experience_system import ExperienceSystem


class ExplorationSystem:
    EVENTS = (
        "上古傳承",
        "遭遇妖獸",
        "找到丹藥",
        "領悟天地靈氣",
        "發現靈石礦脈",
        "發現靈藥圃",
    )

    def __init__(self, choice=None, randint=None, experience_system=None):
        self.choice = choice or random.choice
        self.randint = randint or random.randint
        self.experience_system = experience_system or ExperienceSystem()

    def explore(self, player, item_system, level_system):
        if not isinstance(player, Player):
            return False, "【探索失敗】找不到有效的修士資料。"
        if item_system is None or level_system is None:
            return False, "【探索失敗】探索系統尚未完整連接。"

        event_name = self.choice(self.EVENTS)

        if event_name == "上古傳承":
            _, _, message = self.experience_system.add_exp(player, 100)
        elif event_name == "遭遇妖獸":
            damage = self.randint(10, 30)
            actual_damage = min(damage, player.hp)
            player.hp = max(0, player.hp - damage)
            message = f"遭遇妖獸，受到 {actual_damage} 點傷害。"
        elif event_name == "找到丹藥":
            item_system.add_item("gathering_pill", 1)
            self._sync_inventory(player, item_system)
            message = "在石縫中找到一枚聚氣丹。"
        elif event_name == "領悟天地靈氣":
            message = self._gain_cultivation(player, level_system, 30)
        elif event_name == "發現靈石礦脈":
            stones = self.randint(20, 50)
            item_system.add_item("spirit_stone", stones)
            self._sync_inventory(player, item_system)
            message = f"發現靈石礦脈，取得 {stones} 枚靈石。"
        else:
            grass = self.randint(3, 8)
            item_system.add_item("spirit_grass", grass)
            self._sync_inventory(player, item_system)
            message = f"發現靈藥圃，採得 {grass} 株靈藥草。"

        return True, f"【探索・{event_name}】{message}"

    @staticmethod
    def _gain_cultivation(player, level_system, amount):
        realm, cultivation, message = level_system.add_cultivation(
            player.realm,
            player.cultivation,
            amount,
        )
        player.realm = realm
        player.cultivation = cultivation
        return message

    @staticmethod
    def _sync_inventory(player, item_system):
        player.inventory = item_system.get_save_data()
        player.spirit_stone = player.inventory.get("spirit_stone", 0)

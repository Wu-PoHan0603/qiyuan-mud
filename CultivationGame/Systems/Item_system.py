from Systems.data_loader import load_items


class ItemSystem:
    """管理物品定義、背包數量、使用與裝備行為。"""

    STARTING_ITEMS = {
        "spirit_stone": 100,
        "spirit_grass": 50,
    }

    def __init__(self, item_database=None):
        self.item_database = item_database or load_items()
        self.inventory = {
            item_id: self.STARTING_ITEMS.get(item_id, 0)
            for item_id in self.item_database
        }

    def use_or_equip(self, player, item_id, level_system):
        item = self.item_database.get(item_id)
        if item is None:
            return False, "不存在的物品。"
        if self.get_item_count(item_id) <= 0:
            return False, f"{item['name']}數量不足。"

        if item["type"] == "weapon":
            player.weapon = item["name"]
            player.weapon_atk = item["attack"]
            return True, f"已裝備{item['name']}。"
        if item["type"] == "armor":
            player.armor = item["name"]
            player.armor_def = item["defense"]
            return True, f"已裝備{item['name']}。"
        if item["type"] == "skill":
            player.skill = item["name"]
            player.skill_power = item["power"]
            return True, f"已切換技能為{item['name']}。"
        if item_id != "gathering_pill":
            return False, "此物品不能直接使用或裝備。"

        realm, cultivation, message = level_system.add_cultivation(
            player.realm, player.cultivation, 50
        )
        if realm == player.realm and cultivation == player.cultivation:
            return False, message
        self.remove_item(item_id, 1)
        player.realm = realm
        player.cultivation = cultivation
        player.inventory = self.get_save_data()
        return True, f"服用聚氣丹。{message}"

    def get_item_name(self, item_id):
        return self.item_database.get(item_id, {"name": item_id})["name"]

    def add_item(self, item_id, amount=1):
        if amount <= 0 or item_id not in self.inventory:
            return False
        self.inventory[item_id] += amount
        return True

    def remove_item(self, item_id, amount=1):
        if amount <= 0 or self.inventory.get(item_id, 0) < amount:
            return False
        self.inventory[item_id] -= amount
        return True

    def get_item_count(self, item_id):
        return self.inventory.get(item_id, 0)

    def get_save_data(self):
        return dict(self.inventory)

    def load_save_data(self, saved_inventory):
        if not saved_inventory:
            return
        for item_id in self.inventory:
            if item_id in saved_inventory:
                value = saved_inventory[item_id]
                if isinstance(value, int) and not isinstance(value, bool) and value >= 0:
                    self.inventory[item_id] = value

    def reload_data(self, item_database):
        if not isinstance(item_database, dict):
            return False, "物品資料格式錯誤。"
        if set(item_database) != set(self.item_database):
            return False, "物品 ID 有增減，為避免背包資料遺失已取消重新載入。"
        self.item_database = {
            item_id: dict(item)
            for item_id, item in item_database.items()
        }
        return True, "物品資料已重新載入。"

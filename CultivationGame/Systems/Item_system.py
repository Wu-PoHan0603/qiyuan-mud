# Systems/Item_system.py
class ItemSystem:
    """背包與道具數量管理。"""

    def __init__(self):
        self.item_database = {
            "spirit_stone": {
                "name": "靈石",
                "type": "currency",
                "desc": "修仙界通用貨幣。",
            },
            "foundation_pill": {
                "name": "築基丹",
                "type": "potion",
                "desc": "突破築基期必備丹藥。",
            },
            "spirit_grass": {
                "name": "靈藥草",
                "type": "material",
                "desc": "煉丹基礎材料。",
            },
            "gathering_pill": {
                "name": "聚氣丹",
                "type": "potion",
                "desc": "服用後增加修為。",
            },
        }

        # 為方便測試煉丹，初始給予部分材料
        self.inventory = {
            "spirit_stone": 100,
            "foundation_pill": 0,
            "spirit_grass": 50,
            "gathering_pill": 0,
        }

    def get_item_name(self, item_id):
        return self.item_database.get(
            item_id,
            {"name": item_id},
        )["name"]

    def add_item(self, item_id, amount=1):
        if amount <= 0:
            return False

        if item_id not in self.inventory:
            print(f"【背包】不存在道具：{item_id}")
            return False

        self.inventory[item_id] += amount
        print(
            f"【背包】獲得"
            f"【{self.get_item_name(item_id)}】x{amount}"
        )
        return True

    def remove_item(self, item_id, amount=1):
        if amount <= 0:
            return False

        current = self.inventory.get(item_id, 0)

        if current < amount:
            print(
                f"【背包】"
                f"【{self.get_item_name(item_id)}】不足。"
            )
            return False

        self.inventory[item_id] -= amount
        print(
            f"【背包】消耗"
            f"【{self.get_item_name(item_id)}】x{amount}"
        )
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
                self.inventory[item_id] = int(
                    saved_inventory[item_id]
                )

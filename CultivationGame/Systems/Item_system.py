#背包系統
# Systems/Item_system.py

class ItemSystem:
    def __init__(self):
        # 1. 定義遊戲中所有道具的「資料庫」原型
        self.item_database = {
            "spirit_stone": {"name": "靈石", "type": "currency", "desc": "修仙界通用的貨幣，蘊含微量靈氣。"},
            "foundation_pill": {"name": "築基丹", "type": "potion", "desc": "練氣九層大圓滿突破至築基期必備之丹藥。"},
            "spirit_grass": {"name": "靈藥草", "type": "material", "desc": "煉製普通丹藥的基礎材料。"},
            "gathering_pill": {"name": "聚氣丹", "type": "potion", "desc": "服用後可瞬間增加 50 點修為。"}
        }
        
        # 2. 玩家的初始背包（數量皆為 0）
        self.inventory = {
            "spirit_stone": 10,       # 初始贈送 10 顆靈石
            "foundation_pill": 0,
            "spirit_grass": 0,
            "gathering_pill": 0
        }

    def add_item(self, item_id, amount=1):
        """
        增加背包中的道具數量
        :param item_id: 道具ID (字串)
        :param amount: 增加數量 (整數)
        """
        if item_id in self.inventory:
            self.inventory[item_id] += amount
            item_name = self.item_database[item_id]["name"]
            print(f"【內府背包】獲得了【{item_name}】x{amount}")
            return True
        else:
            print(f"【內府背包】天道資料庫中不存在此道具: {item_id}")
            return False

    def remove_item(self, item_id, amount=1):
        """
        消耗背包中的道具
        :return: 消耗成功返回 True，數量不足返回 False
        """
        if item_id in self.inventory and self.inventory[item_id] >= amount:
            self.inventory[item_id] -= amount
            item_name = self.item_database[item_id]["name"]
            print(f"【內府背包】消耗了【{item_name}】x{amount}")
            return True
        else:
            item_name = self.item_database.get(item_id, {}).get("name", "未知道具")
            print(f"【內府背包】無法消耗！【{item_name}】數量不足（目前擁有: {self.inventory.get(item_id, 0)}）")
            return False

    def get_item_count(self, item_id):
        """查詢某道具當前數量"""
        return self.inventory.get(item_id, 0)

    def get_save_data(self):
        """打包背包數據，提供給存檔系統寫入 JSON"""
        return self.inventory

    def load_save_data(self, saved_inventory):
        """從存檔 JSON 還原背包數據"""
        if saved_inventory:
            # 採用遞補方式，防止舊存檔缺少新加入的道具種類
            for item_id, count in saved_inventory.items():
                if item_id in self.inventory:
                    self.inventory[item_id] = count

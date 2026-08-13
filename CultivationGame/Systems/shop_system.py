class ShopSystem:
    PRICES = {
        "spirit_grass": 8,
        "gathering_pill": 20, "foundation_pill": 100,
        "wood_sword": 30, "iron_sword": 100,
        "steel_sword": 250, "dark_iron_sword": 500,
        "cloth_armor": 30, "copper_armor": 80,
        "iron_armor": 160, "golden_cicada_armor": 300,
        "fireball_scroll": 100, "earth_spike_scroll": 250,
        "ice_arrow_scroll": 500, "thunder_strike_scroll": 800,
    }

    def buy(self, player, item_system, item_id):
        price = self.PRICES.get(item_id)
        if price is None or item_id not in item_system.item_database:
            return False, "商品不存在。"
        if item_system.get_item_count("spirit_stone") < price:
            return False, "靈石不足。"
        if not item_system.remove_item("spirit_stone", price):
            return False, "交易失敗。"
        if not item_system.add_item(item_id, 1):
            item_system.add_item("spirit_stone", price)
            return False, "交易失敗。"
        self._sync(player, item_system)
        return True, f"購買【{item_system.get_item_name(item_id)}】成功。"

    def sell(self, player, item_system, item_id):
        price = self.PRICES.get(item_id)
        if price is None or item_id not in item_system.item_database:
            return False, "商品不存在。"
        if item_system.get_item_count(item_id) <= 0:
            return False, "物品數量不足。"
        item = item_system.item_database[item_id]
        is_equipped_weapon = (
            item.get("type") == "weapon" and player.weapon == item.get("name")
        )
        is_equipped_armor = (
            item.get("type") == "armor" and player.armor == item.get("name")
        )
        if (
            is_equipped_weapon or is_equipped_armor
        ) and item_system.get_item_count(item_id) == 1:
            return False, "此物品正在裝備中，不能賣出最後一件。"
        sell_price = max(1, price // 2)
        if not item_system.remove_item(item_id, 1):
            return False, "交易失敗。"
        item_system.add_item("spirit_stone", sell_price)
        self._sync(player, item_system)
        return True, f"出售成功，取得 {sell_price} 枚靈石。"

    @staticmethod
    def _sync(player, item_system):
        player.inventory = item_system.get_save_data()
        player.spirit_stone = player.inventory["spirit_stone"]

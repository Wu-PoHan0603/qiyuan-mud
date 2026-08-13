import random

from Objects.Player import Player


class CultivationSystem:
    """處理修煉事件與修為增加規則。"""

    def __init__(self, randint=None):
        self.randint = randint or random.randint

    def cultivate(self, player, level_system):
        if not isinstance(player, Player) or level_system is None:
            return False, "【修煉失敗】修士資料或境界系統異常。"

        roll = self.randint(1, 100)
        if roll <= 60:
            event_name = "一般修煉"
            gain = self.randint(10, 30)
        elif roll <= 90:
            event_name = "爆擊修煉"
            gain = self.randint(40, 80)
        else:
            event_name = "天道頓悟"
            gain = self.randint(120, 200)

        realm, cultivation, result = level_system.add_cultivation(
            player.realm,
            player.cultivation,
            gain,
        )
        player.realm = realm
        player.cultivation = cultivation
        player.realm_index = player._get_realm_index(realm)
        return True, f"【{event_name}】獲得 {gain} 點修為。{result}"

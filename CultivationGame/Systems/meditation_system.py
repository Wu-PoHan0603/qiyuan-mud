import random

from Objects.Player import Player


class MeditationSystem:
    """處理洞府打坐恢復 HP 與 MP 的規則。"""

    def __init__(self, randint=None):
        self.randint = randint or random.randint

    def meditate(self, player):
        if not isinstance(player, Player):
            return False, 0, "【打坐失敗】找不到有效的修士資料。"

        if (
            player.max_mp <= 0
            or player.mp < 0
            or player.mp > player.max_mp
            or player.max_hp <= 0
            or player.hp < 0
            or player.hp > player.max_hp
        ):
            return False, 0, "【打坐失敗】氣血或法力資料異常。"

        if player.mp >= player.max_mp and player.hp >= player.max_hp:
            return False, 0, "【打坐】氣血與法力皆滿，無需繼續調息。"

        actual_mp_recovery = 0
        if player.mp < player.max_mp:
            mp_recovery = self.randint(20, 50)
            actual_mp_recovery = min(
                mp_recovery,
                player.max_mp - player.mp,
            )
            player.mp += actual_mp_recovery

        actual_hp_recovery = 0
        if player.hp < player.max_hp:
            hp_recovery = self.randint(10, 30)
            actual_hp_recovery = min(
                hp_recovery,
                player.max_hp - player.hp,
            )
            player.hp += actual_hp_recovery

        message = (
            f"【打坐調息】氣血恢復 {actual_hp_recovery} 點，"
            f"法力恢復 {actual_mp_recovery} 點。"
        )
        return True, actual_mp_recovery, message

from Objects.Player import Player


class FastTrainingSystem:
    ATTEMPTS = 10

    def train(self, player, level_system, cultivation_system):
        if not isinstance(player, Player):
            return False, "找不到有效的修士資料。"
        if level_system is None or cultivation_system is None:
            return False, "修練系統尚未完整連接。"

        completed = 0
        for _ in range(self.ATTEMPTS):
            maximum = level_system.get_max_cultivation(player.realm)
            if (
                player.realm in level_system.BREAKTHROUGH_PILLS
                and player.cultivation >= maximum
            ):
                break
            ok, _ = cultivation_system.cultivate(player, level_system)
            if not ok:
                break
            completed += 1

        if completed == 0:
            return False, "已達大境界瓶頸，請先取得並服用對應突破丹。"
        return True, f"極速修練完成 {completed} 次，目前境界為{player.realm}。"

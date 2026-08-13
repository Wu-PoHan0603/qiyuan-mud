from Objects.Player import Player


class ExperienceSystem:
    """Manage ordinary character EXP separately from realm cultivation."""

    BASE_EXP = 100
    HP_PER_LEVEL = 10
    MP_PER_LEVEL = 5

    @classmethod
    def required_exp(cls, level):
        if not isinstance(level, int) or isinstance(level, bool) or level < 1:
            raise ValueError("等級必須是正整數。")
        return cls.BASE_EXP * level

    def add_exp(self, player, amount):
        if not isinstance(player, Player):
            return False, 0, "找不到有效的修士資料。"
        if not isinstance(amount, int) or isinstance(amount, bool) or amount <= 0:
            return False, 0, "EXP 數量必須是正整數。"

        player.exp += amount
        levels_gained = 0
        while player.exp >= self.required_exp(player.level):
            player.exp -= self.required_exp(player.level)
            player.level += 1
            levels_gained += 1

        if levels_gained:
            hp_gain = self.HP_PER_LEVEL * levels_gained
            mp_gain = self.MP_PER_LEVEL * levels_gained
            player.max_hp += hp_gain
            player.hp = min(player.max_hp, player.hp + hp_gain)
            player.max_mp += mp_gain
            player.mp = min(player.max_mp, player.mp + mp_gain)

        if levels_gained:
            return (
                True,
                levels_gained,
                f"獲得 {amount} EXP，提升 {levels_gained} 級至等級 {player.level}。",
            )
        return True, 0, f"獲得 {amount} EXP。"

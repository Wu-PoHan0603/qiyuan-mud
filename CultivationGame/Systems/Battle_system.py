from Objects.Boss import Boss
from Objects.Player import Player
from Systems.Reward_system import RewardSystem
from Systems.data_loader import load_bosses, load_skills


class BattleSystem:
    SKILL_MP_COST = 20

    def __init__(self, reward_system=None, bosses=None, skills=None):
        self.reward_system = reward_system or RewardSystem()
        self.bosses = bosses or load_bosses()
        self.skills = skills or load_skills()
        self.battle_finished = False
        self.reward_claimed = False

    def create_boss(self, boss_id="qi_wolf"):
        self.battle_finished = False
        self.reward_claimed = False
        data = self.bosses.get(boss_id)
        if data is None:
            raise ValueError(f"不存在的 Boss：{boss_id}")
        return Boss(
            name=data["name"],
            hp=data["hp"],
            attack=data["attack"],
            reward={
                "exp": data["exp"],
                "spirit_stone": data["spirit_stone"],
                "spirit_grass": data["spirit_grass"],
                "drops": data["drops"],
            },
        )

    def create_boss_for_player(self, player):
        if not isinstance(player, Player):
            raise TypeError("需要有效的修士資料才能選擇 Boss。")
        realm_index = max(0, min(8, player.realm_index))
        for boss_id, data in self.bosses.items():
            if data["realm_index"] == realm_index:
                return self.create_boss(boss_id)
        raise ValueError(f"找不到境界索引 {realm_index} 對應的 Boss。")

    def attack(self, player, boss):
        if not self._can_act(player, boss):
            return False, "戰鬥已結束。"
        level_bonus = max(0, player.level - 1) * 2
        damage = max(1, player.weapon_atk + level_bonus)
        boss.hp = max(0, boss.hp - damage)
        message = f"你造成 {damage} 點傷害。"
        return self._finish_turn(player, boss, message)

    def use_skill(self, player, boss):
        if not self._can_act(player, boss):
            return False, "戰鬥已結束。"
        skill = self.skills.get(player.skill)
        if skill is None:
            return False, "目前技能資料不存在。"
        mp_cost = skill["mp_cost"]
        if player.mp < mp_cost:
            return False, "MP 不足，技能未施放。"
        player.mp -= mp_cost
        level_bonus = max(0, player.level - 1) * 3
        damage = max(1, skill["power"] + level_bonus)
        boss.hp = max(0, boss.hp - damage)
        message = f"施放{player.skill}，造成 {damage} 點傷害。"
        return self._finish_turn(player, boss, message)

    def use_pill(self, player, boss, item_system):
        if not self._can_act(player, boss):
            return False, "戰鬥已結束。"
        if item_system.get_item_count("gathering_pill") <= 0:
            return False, "丹藥不足。"
        if player.hp >= player.max_hp:
            return False, "HP 已滿，未使用丹藥。"
        item_system.remove_item("gathering_pill", 1)
        healing_power = max(30, player.max_hp // 3)
        healed = min(healing_power, player.max_hp - player.hp)
        player.hp += healed
        player.inventory = item_system.get_save_data()
        return self._finish_turn(player, boss, f"服用丹藥，恢復 {healed} HP。")

    def flee(self):
        if self.battle_finished:
            return False, "戰鬥已結束。"
        self.battle_finished = True
        return True, "你已離開戰鬥。"

    def recover_after_defeat(self, player):
        if not isinstance(player, Player):
            return False, "找不到有效的修士資料。"
        if player.hp > 0:
            return False, "修士尚未戰敗，不需要恢復。"
        player.hp = max(1, player.max_hp // 2)
        player.mp = max(player.mp, player.max_mp // 4)
        return True, f"返回洞府療傷，恢復至 {player.hp} HP、{player.mp} MP。"

    def claim_reward(self, player, boss, item_system):
        if not self.battle_finished or not boss.is_dead:
            return False, "尚未擊敗 Boss。"
        if self.reward_claimed:
            return False, "獎勵已領取。"
        self.reward_claimed = True
        return True, self.reward_system.grant_boss_reward(player, item_system, boss)

    def _finish_turn(self, player, boss, message):
        if boss.is_dead:
            self.battle_finished = True
            return True, message + " Boss 已被擊敗。"
        level_defense = max(0, player.level - 1)
        damage = max(1, boss.attack - player.armor_def - level_defense)
        player.hp = max(0, player.hp - damage)
        if player.hp <= 0:
            self.battle_finished = True
            return True, message + f" Boss 反擊 {damage} 點，你已戰敗。"
        return True, message + f" Boss 反擊 {damage} 點。"

    def _can_act(self, player, boss):
        return (
            isinstance(player, Player)
            and isinstance(boss, Boss)
            and not self.battle_finished
            and player.hp > 0
            and not boss.is_dead
        )

    def reload_data(self, bosses, skills):
        if not isinstance(bosses, dict) or set(bosses) != set(self.bosses):
            return False, "Boss ID 有增減，已取消重新載入。"
        if not isinstance(skills, dict) or set(skills) != set(self.skills):
            return False, "技能名稱有增減，已取消重新載入。"
        self.bosses = {boss_id: dict(data) for boss_id, data in bosses.items()}
        self.skills = {name: dict(data) for name, data in skills.items()}
        return True, "Boss 與技能資料已重新載入。"

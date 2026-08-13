import random

from Systems.experience_system import ExperienceSystem


class RewardSystem:
    DROPS = ("gathering_pill", "iron_sword", "iron_armor")

    def __init__(self, choice=None, experience_system=None):
        self.choice = choice or random.choice
        self.experience_system = experience_system or ExperienceSystem()

    def grant_boss_reward(self, player, item_system, boss=None):
        reward = getattr(boss, "reward", {}) or {}
        exp = reward.get("exp", 100)
        spirit_stone = reward.get("spirit_stone", 80)
        spirit_grass = reward.get("spirit_grass", 0)
        drops = tuple(reward.get("drops", self.DROPS)) or self.DROPS
        _, _, exp_message = self.experience_system.add_exp(player, exp)
        item_system.add_item("spirit_stone", spirit_stone)
        if spirit_grass:
            item_system.add_item("spirit_grass", spirit_grass)
        drop = self.choice(drops)
        item_system.add_item(drop, 1)
        player.inventory = item_system.get_save_data()
        player.spirit_stone = player.inventory["spirit_stone"]
        return (
            f"{exp_message} 獲得靈石 {spirit_stone}、靈藥草 {spirit_grass}、"
            f"{item_system.get_item_name(drop)} x1。"
        )

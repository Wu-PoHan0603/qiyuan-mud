import random

from Systems.data_loader import load_recipes


class AlchemySystem:
    RECIPES = load_recipes()

    def __init__(self, randint=None, recipes=None):
        self.randint = randint or random.randint
        self.recipes = recipes or self.RECIPES

    def refine(self, item_system, recipe_id):
        recipe = self.recipes.get(recipe_id)
        if recipe is None:
            return False, "不存在的丹方。"

        missing = []
        for item_id, required in recipe["materials"].items():
            current = item_system.get_item_count(item_id)
            if current < required:
                missing.append(f"{item_system.get_item_name(item_id)} {current}/{required}")
        if missing:
            return False, "材料不足：" + "、".join(missing)

        for item_id, required in recipe["materials"].items():
            item_system.remove_item(item_id, required)

        if self.randint(1, 100) <= recipe["success_rate"]:
            item_system.add_item(recipe_id, 1)
            return True, f"煉丹成功，獲得{recipe['name']} x1。"
        return False, f"煉丹失敗，材料已消耗（成功率 {recipe['success_rate']}%）。"

    def reload_data(self, recipes):
        if not isinstance(recipes, dict) or set(recipes) != set(self.recipes):
            return False, "丹方 ID 有增減，已取消重新載入。"
        self.recipes = {
            recipe_id: dict(recipe)
            for recipe_id, recipe in recipes.items()
        }
        return True, "丹方資料已重新載入。"

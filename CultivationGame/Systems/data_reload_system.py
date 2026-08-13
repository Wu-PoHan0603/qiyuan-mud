from Systems.data_loader import (
    GameDataError,
    load_bosses,
    load_items,
    load_recipes,
    load_skills,
)


class DataReloadSystem:
    def __init__(
        self,
        items_loader=load_items,
        bosses_loader=load_bosses,
        skills_loader=load_skills,
        recipes_loader=load_recipes,
    ):
        self.loaders = {
            "items": items_loader,
            "bosses": bosses_loader,
            "skills": skills_loader,
            "recipes": recipes_loader,
        }

    def validate_all(self):
        try:
            bundle = {
                name: loader()
                for name, loader in self.loaders.items()
            }
            return True, bundle, "JSON 資料驗證完成。"
        except (GameDataError, OSError, TypeError, ValueError) as error:
            return False, None, f"JSON 資料重新載入失敗：{error}"

    @staticmethod
    def apply_all(bundle, item_system, alchemy_system, battle_system):
        if not isinstance(bundle, dict):
            return False, "沒有可套用的資料。"
        compatible = (
            set(bundle.get("items", {})) == set(item_system.item_database)
            and set(bundle.get("recipes", {})) == set(alchemy_system.recipes)
            and set(bundle.get("bosses", {})) == set(battle_system.bosses)
            and set(bundle.get("skills", {})) == set(battle_system.skills)
        )
        if not compatible:
            return False, "資料 ID 有增減，為避免執行中狀態損毀已取消套用。"
        item_system.reload_data(bundle["items"])
        alchemy_system.reload_data(bundle["recipes"])
        battle_system.reload_data(bundle["bosses"], bundle["skills"])
        return True, "JSON 資料已安全重新載入。"

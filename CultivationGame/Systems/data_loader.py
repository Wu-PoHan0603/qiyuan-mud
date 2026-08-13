import json
from pathlib import Path


class GameDataError(ValueError):
    """Raised when a static game-data file has an invalid structure."""


DATA_DIR = Path(__file__).resolve().parent.parent / "data"
ALLOWED_ITEM_TYPES = {"currency", "material", "potion", "weapon", "armor", "skill"}


def _read_json(data_path, label):
    try:
        with data_path.open("r", encoding="utf-8") as file:
            return json.load(file)
    except (OSError, json.JSONDecodeError) as exc:
        raise GameDataError(f"無法讀取{label}資料：{data_path}") from exc


def load_items(path=None):
    data_path = Path(path) if path else DATA_DIR / "items.json"
    data = _read_json(data_path, "物品")

    if not isinstance(data, dict) or not data:
        raise GameDataError("物品資料必須是非空物件。")

    validated = {}
    for item_id, item in data.items():
        if not isinstance(item_id, str) or not isinstance(item, dict):
            raise GameDataError("物品 ID 與內容格式錯誤。")
        name = item.get("name")
        item_type = item.get("type")
        if not isinstance(name, str) or not name.strip():
            raise GameDataError(f"物品 {item_id} 缺少有效名稱。")
        if item_type not in ALLOWED_ITEM_TYPES:
            raise GameDataError(f"物品 {item_id} 類型無效。")
        for field in ("attack", "defense", "power"):
            if field in item and (not isinstance(item[field], int) or item[field] < 0):
                raise GameDataError(f"物品 {item_id} 的 {field} 無效。")
        validated[item_id] = dict(item)
    return validated


def load_bosses(path=None):
    data_path = Path(path) if path else DATA_DIR / "bosses.json"
    data = _read_json(data_path, "Boss")
    if not isinstance(data, dict) or not data:
        raise GameDataError("Boss 資料必須是非空物件。")
    item_ids = set(load_items())
    realm_indices = set()
    for boss_id, boss in data.items():
        if not isinstance(boss_id, str) or not isinstance(boss, dict):
            raise GameDataError("Boss ID 與內容格式錯誤。")
        if not isinstance(boss.get("name"), str):
            raise GameDataError(f"Boss {boss_id} 缺少名稱。")
        realm_index = boss.get("realm_index")
        if (
            not isinstance(realm_index, int)
            or isinstance(realm_index, bool)
            or not 0 <= realm_index <= 8
        ):
            raise GameDataError(f"Boss {boss_id} 的 realm_index 無效。")
        if realm_index in realm_indices:
            raise GameDataError("每個大境界只能設定一個 Boss。")
        realm_indices.add(realm_index)
        for field in ("hp", "attack", "exp", "spirit_stone", "spirit_grass"):
            if not isinstance(boss.get(field), int) or boss[field] < 0:
                raise GameDataError(f"Boss {boss_id} 的 {field} 無效。")
        drops = boss.get("drops")
        if not isinstance(drops, list) or not all(isinstance(x, str) for x in drops):
            raise GameDataError(f"Boss {boss_id} 的掉落資料無效。")
        if set(drops) - item_ids:
            raise GameDataError(f"Boss {boss_id} 包含不存在的掉落物 ID。")
    return data


def load_skills(path=None):
    data_path = Path(path) if path else DATA_DIR / "skills.json"
    data = _read_json(data_path, "技能")
    if not isinstance(data, dict) or not data:
        raise GameDataError("技能資料必須是非空物件。")
    for skill_name, skill in data.items():
        if not isinstance(skill_name, str) or not isinstance(skill, dict):
            raise GameDataError("技能名稱與內容格式錯誤。")
        for field in ("power", "mp_cost"):
            if not isinstance(skill.get(field), int) or skill[field] < 0:
                raise GameDataError(f"技能 {skill_name} 的 {field} 無效。")
    return data


def load_recipes(path=None):
    data_path = Path(path) if path else DATA_DIR / "recipes.json"
    data = _read_json(data_path, "丹方")
    if not isinstance(data, dict) or not data:
        raise GameDataError("丹方資料必須是非空物件。")
    item_database = load_items()
    for recipe_id, recipe in data.items():
        if not isinstance(recipe_id, str) or not isinstance(recipe, dict):
            raise GameDataError("丹方 ID 與內容格式錯誤。")
        if not isinstance(recipe.get("name"), str) or not recipe["name"].strip():
            raise GameDataError(f"丹方 {recipe_id} 缺少名稱。")
        materials = recipe.get("materials")
        if not isinstance(materials, dict) or not materials:
            raise GameDataError(f"丹方 {recipe_id} 缺少材料。")
        if not all(
            isinstance(item_id, str)
            and isinstance(amount, int)
            and not isinstance(amount, bool)
            and amount > 0
            for item_id, amount in materials.items()
        ):
            raise GameDataError(f"丹方 {recipe_id} 的材料格式錯誤。")
        rate = recipe.get("success_rate")
        if not isinstance(rate, int) or isinstance(rate, bool) or not 0 <= rate <= 100:
            raise GameDataError(f"丹方 {recipe_id} 的成功率無效。")
        if recipe_id not in item_database:
            raise GameDataError(f"丹方產物 {recipe_id} 不存在於物品資料。")
        unknown_materials = set(materials) - set(item_database)
        if unknown_materials:
            raise GameDataError(
                f"丹方 {recipe_id} 包含不存在的材料 ID。"
            )
    return data

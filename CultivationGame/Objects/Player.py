# Objects/Player.py


class Player:
    """統一保存玩家資料。"""

    MAX_HP = 100
    MAX_MP = 100
    VALID_SPIRITUAL_ROOTS = {"凡人", "金", "木", "水", "火", "土"}
    INVENTORY_DEFAULTS = {
        "spirit_stone": 0, "foundation_pill": 0,
        "spirit_grass": 0, "gathering_pill": 0,
        "golden_core_pill": 0, "nascent_soul_pill": 0,
        "spirit_transformation_pill": 0, "void_refinement_pill": 0,
        "body_integration_pill": 0, "tribulation_pill": 0,
        "mahayana_pill": 0,
        "wood_sword": 0, "iron_sword": 0,
        "steel_sword": 0, "dark_iron_sword": 0,
        "cloth_armor": 0, "copper_armor": 0,
        "iron_armor": 0, "golden_cicada_armor": 0,
        "fireball_scroll": 0, "earth_spike_scroll": 0,
        "ice_arrow_scroll": 0, "thunder_strike_scroll": 0,
    }
    VALID_ITEM_IDS = set(INVENTORY_DEFAULTS)
    WEAPONS = {"木劍": 5, "鐵劍": 25, "精鋼劍": 50, "玄鐵劍": 100}
    ARMORS = {"布衣": 5, "銅衣": 10, "鐵衣": 20, "金蟬衣": 30}
    SKILLS = {"火球術": 20, "土刺術": 50, "冰箭術": 80, "雷擊術": 100}

    def __init__(
        self,
        name="道友",
        spiritual_root="凡人",
        realm="凡人境界",
        cultivation=0,
        spirit_stone=100,
        hp=100,
        mp=100,
        inventory=None,
        max_hp=100,
        max_mp=100,
        level=1,
        exp=0,
        realm_index=0,
        weapon="木劍",
        weapon_atk=5,
        armor="布衣",
        armor_def=5,
        skill="火球術",
        skill_power=20,
    ):
        self.name = name
        self.spiritual_root = spiritual_root
        self.realm = realm
        self.realm_index = realm_index
        self.level = level
        self.exp = exp
        self.cultivation = cultivation
        self.hp = hp
        self.max_hp = max_hp
        self.mp = mp
        self.max_mp = max_mp
        self.weapon = weapon
        self.weapon_atk = weapon_atk
        self.armor = armor
        self.armor_def = armor_def
        self.skill = skill
        self.skill_power = skill_power

        # 不使用 inventory or {...}
        # 因為空字典 {} 也可能是合法背包資料
        if inventory is None:
            self.inventory = dict(self.INVENTORY_DEFAULTS)
            self.inventory["spirit_stone"] = spirit_stone
            self.inventory["spirit_grass"] = 50
        else:
            self.inventory = dict(self.INVENTORY_DEFAULTS)
            self.inventory.update(inventory)

        # 靈石以 inventory 為主要資料來源
        self.spirit_stone = self.inventory.get(
            "spirit_stone",
            spirit_stone,
        )

    def to_dict(self):
        # 存檔前同步靈石
        self.spirit_stone = self.inventory.get(
            "spirit_stone",
            self.spirit_stone,
        )
        self.realm_index = self._get_realm_index(self.realm)

        return {
            "name": self.name,
            "spiritual_root": self.spiritual_root,
            "level": self.level,
            "exp": self.exp,
            "realm": self.realm,
            "realm_index": self.realm_index,
            "cultivation": self.cultivation,
            "spirit_stone": self.spirit_stone,
            "hp": self.hp,
            "max_hp": self.max_hp,
            "mp": self.mp,
            "max_mp": self.max_mp,
            "weapon": self.weapon,
            "weapon_atk": self.weapon_atk,
            "armor": self.armor,
            "armor_def": self.armor_def,
            "skill": self.skill,
            "skill_power": self.skill_power,
            "inventory": dict(self.inventory),
        }

    @property
    def pill(self):
        return self.inventory.get("gathering_pill", 0)

    @property
    def bag(self):
        return self.inventory

    @classmethod
    def from_dict(cls, data):
        if not isinstance(data, dict):
            raise TypeError("Player data must be a JSON object.")

        name = data.get("name", "道友")
        if not isinstance(name, str):
            raise TypeError("Player name must be text.")
        name = name.strip()
        if not name or len(name) > 8:
            raise ValueError("Player name must contain 1 to 8 characters.")

        spiritual_root = data.get("spiritual_root", "凡人")
        if spiritual_root not in cls.VALID_SPIRITUAL_ROOTS:
            raise ValueError("Unknown spiritual root.")

        realm = data.get("realm", "凡人境界")
        if not cls._is_valid_realm(realm):
            raise ValueError("Unknown realm.")

        expected_realm_index = cls._get_realm_index(realm)
        realm_index = cls._read_int(
            data,
            "realm_index",
            expected_realm_index,
            maximum=8,
        )
        if realm_index != expected_realm_index:
            raise ValueError("realm_index does not match realm.")

        weapon = cls._read_equipment(
            data, "weapon", "weapon_atk", "木劍", cls.WEAPONS
        )
        armor = cls._read_equipment(
            data, "armor", "armor_def", "布衣", cls.ARMORS
        )
        skill = cls._read_equipment(
            data, "skill", "skill_power", "火球術", cls.SKILLS
        )

        saved_inventory = data.get("inventory")

        if saved_inventory is None:
            inventory = dict(cls.INVENTORY_DEFAULTS)
            inventory["spirit_stone"] = cls._read_int(
                data, "spirit_stone", 100
            )
            inventory["spirit_grass"] = 50
        else:
            if not isinstance(saved_inventory, dict):
                raise TypeError("Inventory must be a JSON object.")

            unknown_ids = set(saved_inventory) - cls.VALID_ITEM_IDS
            if unknown_ids:
                raise ValueError("Inventory contains an unknown item ID.")

            fallback_stones = cls._read_int(
                data, "spirit_stone", 100
            )
            inventory = {
                item_id: cls._read_int(
                    saved_inventory,
                    item_id,
                    fallback_stones if item_id == "spirit_stone" else 0,
                )
                for item_id in cls.INVENTORY_DEFAULTS
            }

        max_hp = cls._read_int(
            data,
            "max_hp",
            cls.MAX_HP,
            minimum=1,
        )
        max_mp = cls._read_int(
            data,
            "max_mp",
            cls.MAX_MP,
            minimum=1,
        )

        return cls(
            name=name,
            spiritual_root=spiritual_root,
            level=cls._read_int(data, "level", 1, minimum=1),
            exp=cls._read_int(data, "exp", 0),
            realm=realm,
            realm_index=realm_index,
            cultivation=cls._read_int(data, "cultivation", 0),
            spirit_stone=inventory.get(
                "spirit_stone",
                100,
            ),
            hp=cls._read_int(data, "hp", max_hp, max_hp),
            mp=cls._read_int(data, "mp", max_mp, max_mp),
            inventory=inventory,
            max_hp=max_hp,
            max_mp=max_mp,
            weapon=weapon[0],
            weapon_atk=weapon[1],
            armor=armor[0],
            armor_def=armor[1],
            skill=skill[0],
            skill_power=skill[1],
        )

    @staticmethod
    def _read_int(
        source,
        key,
        default,
        maximum=None,
        minimum=0,
    ):
        value = source.get(key, default)
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError(f"{key} must be an integer.")
        if value < minimum:
            raise ValueError(f"{key} is below its minimum.")
        if maximum is not None and value > maximum:
            raise ValueError(f"{key} exceeds its maximum.")
        return value

    @staticmethod
    def _is_valid_realm(realm):
        if not isinstance(realm, str):
            return False
        if realm == "凡人境界":
            return True
        return any(
            realm == f"{major}期第{layer}層"
            for major in (
                "練氣", "築基", "金丹", "元嬰", "化神",
                "練虛", "合體", "渡劫", "大乘",
            )
            for layer in range(1, 10)
        )

    @staticmethod
    def _get_realm_index(realm):
        major_realms = (
            "練氣", "築基", "金丹", "元嬰", "化神",
            "練虛", "合體", "渡劫", "大乘",
        )
        for index, major_realm in enumerate(major_realms):
            if realm.startswith(major_realm):
                return index
        return 0

    @classmethod
    def _read_equipment(
        cls,
        data,
        name_key,
        value_key,
        default_name,
        database,
    ):
        name = data.get(name_key, default_name)
        if not isinstance(name, str) or name not in database:
            raise ValueError(f"Unknown {name_key}.")
        value = cls._read_int(data, value_key, database[name])
        if value != database[name]:
            raise ValueError(f"{value_key} does not match {name_key}.")
        return name, value

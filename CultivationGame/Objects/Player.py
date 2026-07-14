# Objects/Player.py
class Player:
    """統一保存玩家資料，避免資料散落在 Main、Create、Home。"""

    def __init__(
        self,
        name="道友",
        spiritual_root="凡人",
        realm="凡人境界",
        cultivation=0,
        spirit_stone=10,
        hp=100,
        mp=100,
        inventory=None,
    ):
        self.name = name
        self.spiritual_root = spiritual_root
        self.realm = realm
        self.cultivation = cultivation
        self.spirit_stone = spirit_stone
        self.hp = hp
        self.mp = mp
        self.inventory = inventory or {
            "spirit_stone": spirit_stone,
            "foundation_pill": 0,
            "spirit_grass": 0,
            "gathering_pill": 0,
        }

    def to_dict(self):
        return {
            "name": self.name,
            "spiritual_root": self.spiritual_root,
            "realm": self.realm,
            "cultivation": self.cultivation,
            "spirit_stone": self.spirit_stone,
            "hp": self.hp,
            "mp": self.mp,
            "inventory": dict(self.inventory),
        }

    @classmethod
    def from_dict(cls, data):
        data = data or {}

        inventory = data.get("inventory") or {
            "spirit_stone": data.get("spirit_stone", 10),
            "foundation_pill": 0,
            "spirit_grass": 0,
            "gathering_pill": 0,
        }

        return cls(
            name=data.get("name", "道友"),
            spiritual_root=data.get("spiritual_root", "凡人"),
            realm=data.get("realm", "凡人境界"),
            cultivation=data.get("cultivation", 0),
            spirit_stone=data.get(
                "spirit_stone",
                inventory.get("spirit_stone", 10),
            ),
            hp=data.get("hp", 100),
            mp=data.get("mp", 100),
            inventory=inventory,
        )

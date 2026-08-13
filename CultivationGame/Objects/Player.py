# Objects/Player.py


class Player:
    """統一保存玩家資料。"""

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
    ):
        self.name = name
        self.spiritual_root = spiritual_root
        self.realm = realm
        self.cultivation = cultivation
        self.hp = hp
        self.mp = mp

        # 不使用 inventory or {...}
        # 因為空字典 {} 也可能是合法背包資料
        if inventory is None:
            self.inventory = {
                "spirit_stone": spirit_stone,
                "foundation_pill": 0,
                "spirit_grass": 50,
                "gathering_pill": 0,
            }
        else:
            self.inventory = dict(inventory)

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

        saved_inventory = data.get("inventory")

        if saved_inventory is None:
            inventory = {
                "spirit_stone": data.get(
                    "spirit_stone",
                    100,
                ),
                "foundation_pill": 0,
                "spirit_grass": 50,
                "gathering_pill": 0,
            }
        else:
            inventory = {
                "spirit_stone": int(
                    saved_inventory.get(
                        "spirit_stone",
                        data.get("spirit_stone", 100),
                    )
                ),
                "foundation_pill": int(
                    saved_inventory.get(
                        "foundation_pill",
                        0,
                    )
                ),
                "spirit_grass": int(
                    saved_inventory.get(
                        "spirit_grass",
                        0,
                    )
                ),
                "gathering_pill": int(
                    saved_inventory.get(
                        "gathering_pill",
                        0,
                    )
                ),
            }

        return cls(
            name=data.get("name", "道友"),
            spiritual_root=data.get(
                "spiritual_root",
                "凡人",
            ),
            realm=data.get(
                "realm",
                "凡人境界",
            ),
            cultivation=int(
                data.get("cultivation", 0)
            ),
            spirit_stone=inventory.get(
                "spirit_stone",
                100,
            ),
            hp=int(data.get("hp", 100)),
            mp=int(data.get("mp", 100)),
            inventory=inventory,
        )
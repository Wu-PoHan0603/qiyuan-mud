# Systems/Save_system.py
import json
import os

from Objects.Player import Player


class SaveSystem:
    """負責將 Player 寫入 JSON，以及從 JSON 還原 Player。"""

    def __init__(self):
        self.base_dir = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )
        self.save_file = os.path.join(
            self.base_dir,
            "save_data.json",
        )

    def save_game(self, player):
        try:
            if isinstance(player, Player):
                data = player.to_dict()
            elif isinstance(player, dict):
                # 保留舊程式相容性
                data = player
            else:
                raise TypeError(
                    "save_game() 只接受 Player 或 dict。"
                )

            with open(
                self.save_file,
                "w",
                encoding="utf-8",
            ) as file:
                json.dump(
                    data,
                    file,
                    ensure_ascii=False,
                    indent=4,
                )

            print("【存檔系統】遊戲進度儲存成功！")
            return True

        except Exception as error:
            print(
                f"【存檔系統】儲存失敗：{error}"
            )
            return False

    def load_game(self):
        if not os.path.exists(self.save_file):
            print("【存檔系統】找不到存檔。")
            return None

        try:
            with open(
                self.save_file,
                "r",
                encoding="utf-8",
            ) as file:
                data = json.load(file)

            player = Player.from_dict(data)
            print("【存檔系統】存檔讀取成功！")
            return player

        except Exception as error:
            print(
                f"【存檔系統】讀取失敗：{error}"
            )
            return None

    def has_save(self):
        return os.path.exists(self.save_file)

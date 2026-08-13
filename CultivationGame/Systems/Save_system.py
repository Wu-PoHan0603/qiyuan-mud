# Systems/Save_system.py
import json
import os

from Objects.Player import Player


class SaveSystem:
    """負責將 Player 寫入 JSON，以及從 JSON 還原 Player。"""

    SAVE_VERSION = 1

    def __init__(self):
        self.base_dir = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )
        self.save_dir = os.path.join(self.base_dir, "saves")
        self.save_file = os.path.join(
            self.save_dir,
            "save.json",
        )
        self.debug_save_file = os.path.join(
            self.save_dir,
            "debug_save.json",
        )
        self.legacy_save_file = os.path.join(
            self.base_dir,
            "save_data.json",
        )

    def save_game(self, player):
        temporary_file = None
        try:
            if isinstance(player, Player):
                data = Player.from_dict(player.to_dict()).to_dict()
            elif isinstance(player, dict):
                # 保留舊程式相容性
                data = Player.from_dict(player).to_dict()
            else:
                raise TypeError(
                    "save_game() 只接受 Player 或 dict。"
                )

            save_data = {
                "save_version": self.SAVE_VERSION,
                "player": data,
            }
            os.makedirs(os.path.dirname(self.save_file), exist_ok=True)
            temporary_file = self.save_file + ".tmp"

            with open(
                temporary_file,
                "w",
                encoding="utf-8",
            ) as file:
                json.dump(
                    save_data,
                    file,
                    ensure_ascii=False,
                    indent=4,
                )
            os.replace(temporary_file, self.save_file)

            print("【存檔系統】遊戲進度儲存成功！")
            return True

        except (TypeError, ValueError) as error:
            print(
                f"【存檔系統】玩家資料無效：{error}"
            )
            return False
        except (OSError, UnicodeError) as error:
            if temporary_file and os.path.exists(temporary_file):
                try:
                    os.remove(temporary_file)
                except OSError as cleanup_error:
                    print(
                        f"【存檔系統】暫存檔清理失敗：{cleanup_error}"
                    )
            print(
                f"【存檔系統】儲存失敗：{error}"
            )
            return False

    def load_game(self):
        load_file = self.save_file
        if not os.path.exists(load_file):
            load_file = self.legacy_save_file

        if not os.path.exists(load_file):
            print("【存檔系統】找不到存檔。")
            return None

        try:
            with open(
                load_file,
                "r",
                encoding="utf-8",
            ) as file:
                data = json.load(file)

            if "save_version" in data or "player" in data:
                if data.get("save_version") != self.SAVE_VERSION:
                    raise ValueError("Unsupported save version.")
                player_data = data.get("player")
            else:
                player_data = data

            player = Player.from_dict(player_data)
            print("【存檔系統】存檔讀取成功！")
            return player

        except json.JSONDecodeError as error:
            print(
                f"【存檔系統】JSON 已損毀：{error}"
            )
            return None
        except (TypeError, ValueError) as error:
            print(
                f"【存檔系統】存檔資料無效：{error}"
            )
            return None
        except (OSError, UnicodeError) as error:
            print(
                f"【存檔系統】讀取失敗：{error}"
            )
            return None

    def save_debug_game(self, player):
        """Write a debug slot without changing or replacing the normal slot."""
        normal_save_file = self.save_file
        try:
            self.save_file = self.debug_save_file
            return self.save_game(player)
        finally:
            self.save_file = normal_save_file

    def load_debug_game(self):
        """Load only the debug slot; never fall back to a normal/legacy save."""
        if not os.path.exists(self.debug_save_file):
            return None

        normal_save_file = self.save_file
        legacy_save_file = self.legacy_save_file
        try:
            self.save_file = self.debug_save_file
            self.legacy_save_file = self.debug_save_file
            return self.load_game()
        finally:
            self.save_file = normal_save_file
            self.legacy_save_file = legacy_save_file

    def has_save(self):
        return (
            os.path.exists(self.save_file)
            or os.path.exists(self.legacy_save_file)
        )

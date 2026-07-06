#存檔
import json
import os

class SaveSystem:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.save_dir = os.path.join(self.base_dir, "Saves")
        self.save_file = os.path.join(self.base_dir, "save_data.json")

        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

    def save_game(self, player_data):
        try:
            with open(self.save_file, "w", encoding="utf-8") as f:
                json.dump(player_data, f, indent=4, ensure_ascii=False)
            print("【存檔系統】遊戲進度儲存成功！")
            return True
        except Exception as e:
            print(f"【存檔系統】儲存失敗，錯誤原因: {e}")

            return False
    def load_game(self):
        if not os.path.exists(self.save_file):
            print("【存檔系統】找不到任何存檔檔案。")
            return None
        
        try:
            with open(self.save_file, "r", encoding="utf-8") as f:
                player_data = json.load(f)
            print("【存檔系統】存檔讀取成功！")
            return player_data
        except Exception as e:
            print(f"【存檔系統】讀取失敗，檔案可能損壞: {e}")
            return None

    def has_save(self):
        return os.path.exists(self.save_file)
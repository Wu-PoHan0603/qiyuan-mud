import json
from pathlib import Path

from Objects.GameSettings import GameSettings


class SettingsSystem:
    def __init__(self, settings_file=None):
        base_dir = Path(__file__).resolve().parent.parent
        self.settings_file = Path(settings_file) if settings_file else base_dir / "saves" / "settings.json"
        self.last_error = None

    def load(self):
        self.last_error = None
        if not self.settings_file.exists():
            return GameSettings()
        try:
            with self.settings_file.open("r", encoding="utf-8") as file:
                return GameSettings.from_dict(json.load(file))
        except (
            OSError,
            UnicodeError,
            json.JSONDecodeError,
            TypeError,
            ValueError,
        ) as error:
            self.last_error = str(error)
            return GameSettings()

    def save(self, settings):
        self.last_error = None
        if not isinstance(settings, GameSettings):
            self.last_error = "設定資料型態錯誤。"
            return False
        temporary_file = self.settings_file.with_suffix(
            self.settings_file.suffix + ".tmp"
        )
        try:
            self.settings_file.parent.mkdir(parents=True, exist_ok=True)
            with temporary_file.open("w", encoding="utf-8") as file:
                json.dump(
                    settings.to_dict(),
                    file,
                    ensure_ascii=False,
                    indent=2,
                )
            temporary_file.replace(self.settings_file)
            return True
        except (OSError, UnicodeError) as error:
            self.last_error = str(error)
            if temporary_file.exists():
                try:
                    temporary_file.unlink()
                except OSError as cleanup_error:
                    self.last_error += f"；暫存檔清理失敗：{cleanup_error}"
            return False

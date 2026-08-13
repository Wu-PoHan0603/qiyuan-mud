import wave
from pathlib import Path

import pygame


class AudioManager:
    """Owns scene music and safely degrades when audio is unavailable."""

    TRACKS = {
        "MENU": "background_theme.wav",
        "CREATE": "background_theme.wav",
        "HOME": "cultivator_home_theme.wav",
        "STATUS": "cultivator_home_theme.wav",
        "BAG": "cultivator_home_theme.wav",
        "ALCHEMY": "cultivator_home_theme.wav",
        "SETTINGS": "cultivator_home_theme.wav",
        "MEDITATE": "meditation_theme.wav",
        "SHOP": "shop_theme.wav",
        "BATTLE": "battle_theme.wav",
    }

    def __init__(self, base_dir, volume=100):
        self.audio_dir = Path(base_dir) / "Assets" / "Audio"
        self.volume = max(0, min(100, int(volume)))
        self.enabled = pygame.mixer.get_init() is not None
        self.current_key = None
        self.last_error = None

    def validate_all(self):
        errors = []
        for filename in set(self.TRACKS.values()):
            path = self.audio_dir / filename
            try:
                with wave.open(str(path), "rb") as audio:
                    if audio.getnchannels() not in (1, 2):
                        raise ValueError("聲道數不支援")
                    if audio.getframerate() <= 0 or audio.getnframes() <= 0:
                        raise ValueError("音訊內容為空")
            except (FileNotFoundError, OSError, EOFError, wave.Error, ValueError) as error:
                errors.append(f"{filename}: {error}")
        self.last_error = "；".join(errors) if errors else None
        return not errors, self.last_error or "音訊資源驗證完成。"

    def play_scene(self, scene_key):
        filename = self.TRACKS.get(scene_key)
        if filename is None:
            return False, "場景沒有設定音樂。"
        if not self.enabled:
            return False, "音效裝置不可用，已靜音繼續。"
        if self.current_key == scene_key and pygame.mixer.music.get_busy():
            return True, "音樂已在播放。"
        try:
            pygame.mixer.music.load(str(self.audio_dir / filename))
            pygame.mixer.music.set_volume(self.volume / 100)
            pygame.mixer.music.play(-1)
            self.current_key = scene_key
            self.last_error = None
            return True, f"播放音樂：{filename}"
        except (FileNotFoundError, OSError, pygame.error) as error:
            self.last_error = f"音樂播放失敗：{error}"
            return False, self.last_error

    def set_volume(self, volume):
        self.volume = max(0, min(100, int(volume)))
        if self.enabled:
            pygame.mixer.music.set_volume(self.volume / 100)

    def reload(self):
        ok, message = self.validate_all()
        if not ok:
            return False, message
        current = self.current_key
        self.current_key = None
        if current is not None:
            return self.play_scene(current)
        return True, "音訊資源已安全重新載入。"

    def stop(self):
        if self.enabled:
            pygame.mixer.music.stop()
        self.current_key = None

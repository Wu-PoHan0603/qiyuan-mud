class GameSettings:
    FPS_OPTIONS = (30, 60, 120)
    VOLUME_OPTIONS = (0, 25, 50, 75, 100)

    def __init__(self, fps=60, master_volume=100, fullscreen=False):
        if fps not in self.FPS_OPTIONS:
            raise ValueError("FPS 設定無效。")
        if (
            not isinstance(master_volume, int)
            or isinstance(master_volume, bool)
            or not 0 <= master_volume <= 100
        ):
            raise ValueError("音量必須是 0 到 100 的整數。")
        if not isinstance(fullscreen, bool):
            raise TypeError("全螢幕設定必須是布林值。")
        self.fps = fps
        self.master_volume = master_volume
        self.fullscreen = fullscreen

    def to_dict(self):
        return {
            "fps": self.fps,
            "master_volume": self.master_volume,
            "fullscreen": self.fullscreen,
        }

    @classmethod
    def from_dict(cls, data):
        if not isinstance(data, dict):
            raise TypeError("設定資料必須是 JSON 物件。")
        return cls(
            fps=data.get("fps", 60),
            master_volume=data.get("master_volume", 100),
            fullscreen=data.get("fullscreen", False),
        )

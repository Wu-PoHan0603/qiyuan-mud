from pathlib import Path

import pygame


class AssetManager:
    """Loads and atomically reloads project-owned background images."""

    BACKGROUNDS = {
        "MENU": "main_menu_mountains.png",
        "CREATE": "ascension_gate.png",
        "HOME": "cultivator_home.png",
        "STATUS": "meditation_terrace.png",
        "BAG": "ancient_sect_ruins.png",
        "ALCHEMY": "alchemy_chamber.png",
        "SHOP": "immortal_market.png",
        "SETTINGS": "cultivator_home.png",
        "BATTLE": "storm_battle_arena.png",
        "BATTLE_DEMON": "demon_boss_lair.png",
        "EXPLORE": "secret_realm_forest.png",
        "ASCENSION": "ascension_gate.png",
    }

    def __init__(self, base_dir, size):
        self.asset_dir = Path(base_dir) / "Assets" / "Background"
        self.size = tuple(size)
        self.backgrounds = {}
        self.last_error = None

    def load_all(self):
        loaded = {}
        errors = []
        for key, filename in self.BACKGROUNDS.items():
            try:
                loaded[key] = self._load_image(self.asset_dir / filename)
            except (FileNotFoundError, OSError, pygame.error) as error:
                loaded[key] = self._fallback(key)
                errors.append(f"{filename}: {error}")
        self.backgrounds = loaded
        self.last_error = "；".join(errors) if errors else None
        return not errors, self.last_error or "背景資源載入完成。"

    def reload_all(self):
        candidate = {}
        try:
            for key, filename in self.BACKGROUNDS.items():
                candidate[key] = self._load_image(self.asset_dir / filename)
        except (FileNotFoundError, OSError, pygame.error) as error:
            self.last_error = f"背景重新載入失敗：{error}"
            return False, self.last_error
        self.backgrounds = candidate
        self.last_error = None
        return True, "背景資源已安全重新載入。"

    def get_background(self, key):
        return self.backgrounds.get(key) or self._fallback(key)

    def _load_image(self, path):
        image = pygame.image.load(str(path)).convert()
        return pygame.transform.smoothscale(image, self.size)

    def _fallback(self, key):
        surface = pygame.Surface(self.size)
        colors = {
            "BATTLE": (35, 18, 18),
            "BATTLE_DEMON": (35, 12, 18),
            "ALCHEMY": (35, 22, 18),
            "SHOP": (28, 24, 35),
        }
        surface.fill(colors.get(key, (15, 20, 30)))
        return surface


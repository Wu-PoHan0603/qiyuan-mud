"""Read-only release readiness checks for the Qiyuan cultivation RPG."""

import json
import sys
import wave
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent


def check_release(project_dir=PROJECT_DIR):
    root = Path(project_dir)
    results = []

    def record(name, passed, detail=""):
        results.append((name, bool(passed), str(detail)))

    record("Python 3.10+", sys.version_info >= (3, 10), sys.version.split()[0])
    try:
        import pygame
        record("Pygame import", True, pygame.version.ver)
    except ImportError as error:
        record("Pygame import", False, error)

    for directory in ("Assets", "Font", "Objects", "Scenes", "Systems", "Ui", "data", "saves"):
        record(f"Directory {directory}", (root / directory).is_dir())
    for filename in ("Main.py", "SceneManager.py", "Requirements.txt"):
        record(f"Entry {filename}", (root / filename).is_file())

    fonts = list((root / "Font").glob("*.ttf"))
    record("Font asset", bool(fonts), fonts[0].name if fonts else "missing")

    for filename in ("items.json", "bosses.json", "skills.json", "recipes.json"):
        path = root / "data" / filename
        try:
            data = json.loads(path.read_text(encoding="utf-8-sig"))
            record(f"JSON {filename}", isinstance(data, dict) and bool(data))
        except (OSError, UnicodeError, json.JSONDecodeError) as error:
            record(f"JSON {filename}", False, error)

    backgrounds = list((root / "Assets" / "Background").glob("*.png"))
    generated = [path for path in backgrounds if path.name != "Background.png"]
    record("Generated backgrounds", len(generated) == 10, len(generated))

    audio_files = list((root / "Assets" / "Audio").glob("*.wav"))
    audio_ok = len(audio_files) == 5
    for path in audio_files:
        try:
            with wave.open(str(path), "rb") as audio:
                audio_ok = audio_ok and audio.getnframes() > 0
        except (OSError, EOFError, wave.Error):
            audio_ok = False
    record("Audio tracks", audio_ok, len(audio_files))
    return results


def main():
    results = check_release()
    for name, passed, detail in results:
        status = "PASS" if passed else "FAIL"
        suffix = f" ({detail})" if detail else ""
        print(f"[{status}] {name}{suffix}")
    failed = [result for result in results if not result[1]]
    print(f"\n{len(results) - len(failed)}/{len(results)} checks passed.")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())

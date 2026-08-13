import pygame

from Objects.GameSettings import GameSettings
from Scenes.BaseScene import BaseScene
from Ui.Button import Button
from Ui.visuals import draw_panel, draw_shadow_text, draw_wrapped_text


class SettingsScene(BaseScene):
    def __init__(self, width, height, font_path, settings_system, settings, audio_manager=None):
        self.width = width
        self.height = height
        self.font_path = font_path
        self.settings_system = settings_system
        self.settings = settings
        self.audio_manager = audio_manager
        self.message = "調整後會自動儲存。"
        self.btn_fps = Button(350, 150, 300, 48, "切換 FPS", font_path, 22)
        self.btn_volume = Button(350, 235, 300, 48, "調整音量", font_path, 22)
        self.btn_fullscreen = Button(350, 320, 300, 48, "切換全螢幕", font_path, 22)
        self.btn_reset = Button(350, 405, 300, 48, "恢復預設值", font_path, 22)
        self.btn_back = Button(390, 610, 220, 50, "返回洞府", font_path, 22)

    def handle_event(self, event):
        if self.btn_fps.is_clicked(event):
            options = self.settings.FPS_OPTIONS
            index = options.index(self.settings.fps)
            self.settings.fps = options[(index + 1) % len(options)]
            self._save_current(f"FPS 已調整為 {self.settings.fps}。")
            return None
        if self.btn_volume.is_clicked(event):
            options = self.settings.VOLUME_OPTIONS
            current = self.settings.master_volume
            index = options.index(current) if current in options else -1
            self.settings.master_volume = options[(index + 1) % len(options)]
            self._save_current(f"音量已調整為 {self.settings.master_volume}%。")
            return None
        if self.btn_fullscreen.is_clicked(event):
            self.settings.fullscreen = not self.settings.fullscreen
            mode = "開啟" if self.settings.fullscreen else "關閉"
            self._save_current(f"全螢幕已{mode}，下次啟動套用。")
            return None
        if self.btn_reset.is_clicked(event):
            defaults = GameSettings()
            self.settings.fps = defaults.fps
            self.settings.master_volume = defaults.master_volume
            self.settings.fullscreen = defaults.fullscreen
            self._save_current("設定已恢復預設值。")
            return None
        if self.btn_back.is_clicked(event):
            return "HOME"
        return None

    def _save_current(self, success_message):
        if self.audio_manager is not None:
            self.audio_manager.set_volume(self.settings.master_volume)
        if self.settings_system.save(self.settings):
            self.message = success_message
        else:
            self.message = "設定儲存失敗，請檢查檔案權限。"

    def update(self):
        self.btn_fps.update()
        self.btn_volume.update()
        self.btn_fullscreen.update()
        self.btn_reset.update()
        self.btn_back.update()

    def _draw_text(self, screen, text, size, x, y, color=(235, 235, 225)):
        font = pygame.font.Font(self.font_path, size)
        draw_shadow_text(screen, font, text, color, (x, y))

    def draw(self, screen):
        self.draw_background(screen, (22, 27, 35))
        draw_panel(screen, (300, 30, 400, 525), (16, 23, 31, 220), (190, 160, 95, 235), 2, 14)
        self._draw_text(screen, "系統設置", 40, self.width // 2, 65, (225, 190, 120))
        self._draw_text(screen, f"FPS：{self.settings.fps}", 25, self.width // 2, 125)
        self._draw_text(screen, f"音量：{self.settings.master_volume}%", 25, self.width // 2, 215)
        mode = "開啟" if self.settings.fullscreen else "關閉"
        self._draw_text(screen, f"全螢幕：{mode}", 25, self.width // 2, 300)
        draw_wrapped_text(
            screen, pygame.font.Font(self.font_path, 19), self.message,
            (195, 225, 195), (325, 500, 350, 42), max_lines=2
        )
        self.btn_fps.draw(screen)
        self.btn_volume.draw(screen)
        self.btn_fullscreen.draw(screen)
        self.btn_reset.draw(screen)
        self.btn_back.draw(screen)

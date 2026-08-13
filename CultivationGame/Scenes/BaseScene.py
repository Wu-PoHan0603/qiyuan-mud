#主畫面
import pygame


class BaseScene:

    def set_background(self, background, shade_alpha=115):
        self.background = background
        self.background_shade_alpha = shade_alpha

    def draw_background(self, screen, fallback_color=(15, 20, 30)):
        background = getattr(self, "background", None)
        if background is None:
            screen.fill(fallback_color)
            return
        screen.blit(background, (0, 0))
        shade = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        shade.fill((0, 0, 0, getattr(self, "background_shade_alpha", 115)))
        screen.blit(shade, (0, 0))

    def enter(self):
        """進入場景"""
        pass

    def exit(self):
        """離開場景"""
        pass

    def handle_event(self, event):
        """事件"""
        return None

    def update(self):
        """更新"""
        pass

    def draw(self, screen):
        """畫面"""
        pass

import pygame


class ProgressBar:
    """Display-only progress bar for HP, MP, EXP, and cultivation."""

    def __init__(
        self,
        x,
        y,
        width,
        height,
        fill_color,
        background_color=(45, 45, 45),
        border_color=(220, 220, 220),
    ):
        self.rect = pygame.Rect(x, y, width, height)
        self.fill_color = fill_color
        self.background_color = background_color
        self.border_color = border_color
        self.ratio = 0.0

    def set_value(self, value, maximum):
        if maximum <= 0:
            self.ratio = 0.0
            return
        self.ratio = max(0.0, min(1.0, value / maximum))

    def draw(self, surface):
        background = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        background.fill((*self.background_color, 225))
        surface.blit(background, self.rect.topleft)
        fill_rect = self.rect.copy()
        fill_rect.width = round(self.rect.width * self.ratio)
        if fill_rect.width > 0:
            pygame.draw.rect(surface, self.fill_color, fill_rect, border_radius=4)
        pygame.draw.rect(surface, (15, 15, 15), self.rect, 4, border_radius=5)
        pygame.draw.rect(surface, self.border_color, self.rect, 2, border_radius=5)

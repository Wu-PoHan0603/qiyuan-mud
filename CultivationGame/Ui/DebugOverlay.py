import pygame


class DebugOverlay:
    """Draws read-only runtime diagnostics above the current scene."""

    def __init__(self, font_path, debug_system):
        self.font = pygame.font.Font(font_path, 16)
        self.debug_system = debug_system

    def draw(self, surface, state, scene_name, player, fps):
        lines = self.debug_system.build_lines(
            state, scene_name, player, fps
        )
        if not lines:
            return

        lines = tuple(line[:58] for line in lines[:8])
        line_height = 22
        panel = pygame.Surface(
            (330, 18 + line_height * len(lines)),
            pygame.SRCALPHA,
        )
        panel.fill((0, 0, 0, 190))
        for index, line in enumerate(lines):
            rendered = self.font.render(line, True, (120, 255, 160))
            panel.blit(rendered, (10, 8 + index * line_height))
        surface.blit(panel, (10, 10))

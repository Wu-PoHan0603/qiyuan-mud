import pygame


def draw_panel(
    surface,
    rect,
    fill=(18, 24, 30, 210),
    border=(190, 160, 95, 230),
    border_width=2,
    radius=10,
):
    """Draw a reusable translucent panel without owning game state."""
    target = pygame.Rect(rect)
    panel = pygame.Surface(target.size, pygame.SRCALPHA)
    pygame.draw.rect(panel, fill, panel.get_rect(), border_radius=radius)
    pygame.draw.rect(
        panel,
        border,
        panel.get_rect(),
        border_width,
        border_radius=radius,
    )
    surface.blit(panel, target.topleft)


def draw_shadow_text(
    surface,
    font,
    text,
    color,
    position,
    anchor="center",
    shadow=(0, 0, 0),
    offset=(2, 2),
):
    """Render legible text with a compact drop shadow."""
    text = str(text)
    shadow_surface = font.render(text, True, shadow)
    text_surface = font.render(text, True, color)
    rect = text_surface.get_rect()
    shadow_rect = shadow_surface.get_rect()
    setattr(rect, anchor, position)
    setattr(
        shadow_rect,
        anchor,
        (position[0] + offset[0], position[1] + offset[1]),
    )
    surface.blit(shadow_surface, shadow_rect)
    surface.blit(text_surface, rect)
    return rect


def wrap_text(text, font, max_width):
    """Wrap mixed Chinese/Latin text by rendered pixel width."""
    text = str(text)
    if not text:
        return [""]
    lines = []
    current = ""
    for character in text:
        candidate = current + character
        if current and font.size(candidate)[0] > max_width:
            lines.append(current)
            current = character
        else:
            current = candidate
    if current:
        lines.append(current)
    return lines


def draw_wrapped_text(
    surface,
    font,
    text,
    color,
    rect,
    line_spacing=4,
    max_lines=None,
    centered=True,
):
    target = pygame.Rect(rect)
    lines = wrap_text(text, font, target.width)
    if max_lines is not None:
        lines = lines[:max_lines]
    line_height = font.get_linesize() + line_spacing
    for index, line in enumerate(lines):
        y = target.y + index * line_height
        if y + font.get_linesize() > target.bottom:
            break
        x = target.centerx if centered else target.x
        anchor = "midtop" if centered else "topleft"
        draw_shadow_text(surface, font, line, color, (x, y), anchor)
    return lines

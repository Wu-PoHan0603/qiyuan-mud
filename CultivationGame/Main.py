#主程式
import pygame
import os

FPS = 60
WIDTH, HEIGHT = 1000, 700

black = (0, 0, 0)
white = (255, 255, 255)
#遊戲初始化
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("修仙世界")
clock = pygame.time.Clock()

#載入圖片
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
background_img = pygame.image.load(os.path.join(BASE_DIR, "Assets", "Background", "Background.png")).convert()
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
background_img.set_alpha(80)

font_name = os.path.join(BASE_DIR, "Font", "LXGWWenKai-Medium.ttf")

def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, white)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def draw_init():
    screen.blit(background_img, (0,0))
    draw_text(screen, "修仙世界", 64, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, "按任意鍵開始遊戲", 18, WIDTH /2, HEIGHT * 3 / 4)

running = True
#遊戲迴圈
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


#更新遊戲


#螢幕顯示
    screen.fill(black)
    draw_init()
    pygame.display.flip()



pygame.quit()
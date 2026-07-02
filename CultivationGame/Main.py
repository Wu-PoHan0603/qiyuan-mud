#主程式
import pygame
import os

FPS = 60
WIDTH, HEIGHT = 1000, 700

black = (0, 0, 0)
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


def draw_init():
    screen.blit(background_img, (0,0))
    draw_text(screen, "修仙世界", 64, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, "按任意鍵開始遊戲", 18, Width /2, Height * 3 / 4)
    pygame.display.update()

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
    screen.blit(background_img,(0, 0))
    pygame.display.flip()
    draw_init()



pygame.quit()
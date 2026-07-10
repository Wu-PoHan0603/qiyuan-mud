# Scenes/Menu.py
from Scenes.BaseScene import BaseScene
import pygame

class MenuScene(BaseScene):
    def __init__(self, width, height, font_name, background):
        self.widht = width
        self.height = height
        self.font_name = font_name
        self.background = background

    #初始化
    FPS = 60
    WIDTH, HEIGHT = 1000, 700
    black = (0, 0, 0)
    white = (255, 255, 255)
    #遊戲初始化
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("修仙世界")
    clock = pygame.time.Clock()

    def enter(self):
        print("進入 Menu")

    def exit(self):
        print("離開 Menu")

    def handle_event(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN:

            if self.btn_start.is_clicked(event):
                return "CREATE"

            elif self.btn_load.is_clicked(event):
                return "LOAD"

            elif self.btn_quit.is_clicked(event):
                return "QUIT"

        return None

    def update(self):
        pass

    def draw(self, screen):

        screen.blit(self.background, (0,0))

        self.btn_start.draw(screen)
        self.btn_load.draw(screen)
        self.btn_quit.draw(screen)
#主程式
import pygame
import sys
import os
from Ui.Button import Button
from Ui.Button import create_menu_buttons_list 
from Scenes.Menu import MenuScene
from Scenes.Create import CreateScene
from Scenes.Home import HomeScene

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

# Core
scene = {
    "MENU": MenuScene(WIDTH, HEIGHT, font_name, background_img),
    "CREATE": CreateScene(WIDTH, HEIGHT, font_name),
    "HOME": HomeScene(WIDTH, HEIGHT, font_name),
}
current_scene = "MENU"

running = True
while running:
    clock.tick(FPS)
    action_screen = scene.get(current_scene)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if action_screen:
            next_scene = action_screen.handle_event(event)
            if next_scene == "QUIT":
                running = False
            elif next_scene is not None:
                # === 3. 【核心資料流轉】如果從創角準備進入洞府 ===
                if current_scene == "CREATE" and next_scene == "HOME":
                    # 將創角畫面刷新出來的名字與靈根，精確傳遞給 Home 畫面
                    p_name = action_screen.player_name
                    p_root = action_screen.spiritual_root
                    scene["HOME"].enter_scene(p_name, p_root)
                
                current_scene = next_scene  # 切換場景

    # === 4. 按鈕狀態/變色更新區 (帶有安全檢查) ===
    if action_screen:
        if current_scene == "MENU" and hasattr(action_screen, 'buttons'):
            if action_screen.is_started:
                for btn in action_screen.buttons:
                    btn.update()
        elif current_scene == "CREATE" and hasattr(action_screen, 'btn_roll'):
            action_screen.btn_roll.update()
            action_screen.btn_confirm.update()
        elif current_scene == "HOME" and hasattr(action_screen, 'btn_train'):
            # <-- 5. 增加洞府按鈕的懸停變色更新
            action_screen.btn_train.update()
            action_screen.btn_alchemy.update()
            action_screen.btn_back.update()

    # 螢幕顯示
    screen.fill(black)
    if action_screen:
        action_screen.draw(screen)

    pygame.display.flip()

pygame.quit()
sys.exit()
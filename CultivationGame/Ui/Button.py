# 按鈕管理 (Button.py)
import pygame

class Button:
    def __init__(self, x, y, width, height, text, font_path=None, font_size=24):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font_size = font_size

        if font_path:
            self.font = pygame.font.Font(font_path, font_size)
        else:
            self.font = pygame.font.SysFont("Font", "LXGWWenKai-Medium.ttf", font_size)

        self.normal_color = (70, 70, 70)     # 暗灰色
        self.hover_color = (120, 120, 120)   # 亮灰色
        self.text_color = (255, 255, 255)    # 白色
        
        self.current_color = self.normal_color
        self.clicked = False

    def update(self):
        """偵測滑鼠狀態，並回傳是否被點擊 (True/False)"""
        action = False
        pos = pygame.mouse.get_pos()

        # 1. 偵測滑鼠是否懸停在按鈕矩形內
        if self.rect.collidepoint(pos):
            self.current_color = self.hover_color 
            
            # 2. 偵測滑鼠左鍵點擊
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                action = True
        else:
            self.current_color = self.normal_color 

        # 3. 滑鼠放開時重置點擊狀態
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
            
        return action

    def draw(self, surf):
        pygame.draw.rect(surf, self.current_color, self.rect)
        pygame.draw.rect(surf, (255, 255, 255), self.rect, 2)

        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect()
        text_rect.center = self.rect.center 

        surf.blit(text_surf, text_rect)

def create_menu_buttons_list(width, font_name, btn_width=255, btn_height=60):
    """利用迴圈動態建立按鈕清單"""
    btn_x = (width - btn_width) // 2
    buttons = []
    
    # 定義每個按鈕的 (文字, Y座標)
    button_data = [
        ("開始遊戲", 350),
        ("讀取遊戲", 440),
        ("離開遊戲", 530)
    ]
    
    for text, btn_y in button_data:
        # 修正：因為寫在 Button.py 內部，直接使用當前的 Button 類別建立物件
        # 同時把 font_name 透過參數傳進來，避免讀不到
        btn = Button(btn_x, btn_y, btn_width, btn_height, text, font_name, 28)
        buttons.append(btn)
        
    return buttons
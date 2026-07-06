#主程式
import pygame
import sys
import os
from Ui.Button import Button
from Ui.Button import create_menu_buttons_list 
from Scenes.Menu import MenuScene
from Scenes.Create import CreateScene
from Scenes.Home import HomeScene
from Systems.Save_system import SaveSystem
from Systems.Level_system import LevelSystem
from Systems.Item_system import ItemSystem

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
save_sys = SaveSystem()
level_sys = LevelSystem()
item_sys = ItemSystem()

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

                    new_player = {
                        "name": p_name,
                        "spiritual_root": p_root,
                        "realm": "凡人境界",
                        "cultivation": 0,
                        "spirit_stone": 0,
                        "inventory": item_sys.get_save_data(),
                    }
                    save_sys.save_game(new_player)
                    current_scene = next_scene  # 切換場景
                elif current_scene == "MENU" and next_scene == "LOAD":
                    data = save_sys.load_game()
                    if data:
                        scene["HOME"].enter_scene(data["name"], data["spiritual_root"])
                        scene["HOME"].cultivation = data.get("cultivation", 0)
                        scene["HOME"].realm = data.get("realm", "凡人境界")
                        current_scene = "HOME"
                    else:
                        print("【主程式】讀取失敗，沒有存檔紀錄！")
                else:
                    current_scene = next_scene  

    # === 4. 按鈕狀態/變色更新區 (帶有安全檢查) ===
    if action_screen:
        # 🌟【修改點 1】修正縮排，並讓主選單讀取時也支援恢復「儲物袋背包」
        if current_scene == "MENU" and hasattr(action_screen, 'buttons'):
            # 1. 偵測點擊第一個按鈕 [開始遊戲] (索引 0)
            if action_screen.buttons[0].update():
                current_scene = "CREATE"
                
            # 2. 偵測點擊第二個按鈕 [讀取遊戲] (索引 1)
            elif action_screen.buttons[1].update():
                data = save_sys.load_game()  # 呼叫存檔系統讀取 JSON
                if data:
                    # 恢復名字與靈根
                    scene["HOME"].enter_scene(data["name"], data["spiritual_root"])
                    # 恢復最新的九層修為與境界
                    scene["HOME"].cultivation = data.get("cultivation", 0)
                    scene["HOME"].realm = data.get("realm", "凡人境界")
                    # 🌟 新增：讓主選單讀檔時，儲物袋背包數據也能順利還原
                    item_sys.load_save_data(data.get("inventory", {}))
                    
                    current_scene = "HOME"  # 破開時空，直接進入洞府！
                    print("【主選單】成功載入昔日因果與儲物袋，轉入洞府！")
                else:
                    print("【主選單】天書無字！找不到任何存檔紀錄，請先點擊開始遊戲。")
                    
            # 3. 偵測點擊第三個按鈕 [離開遊戲] (索引 2)
            elif action_screen.buttons[2].update():
                running = False

        elif current_scene == "CREATE" and hasattr(action_screen, 'btn_roll'):
            action_screen.btn_roll.update()
            action_screen.btn_confirm.update()
            
        elif current_scene == "HOME" and hasattr(action_screen, 'btn_train'):
            # 🌟【修改點 2】將閉關修煉與「九層大圓滿卡關/消耗築基丹」機制綁定
            if action_screen.btn_train.update():
                # 判定：是否達到練氣九層瓶頸（根據 Level_system 練氣九層上限為 360）
                if "練氣期第9層" in action_screen.realm and action_screen.cultivation >= 360:
                    # 檢查儲物袋中有沒有築基丹
                    if item_sys.get_item_count("foundation_pill") > 0:
                        item_sys.remove_item("foundation_pill", 1)  # 消耗一顆築基丹
                        action_screen.realm = "築基期第1層"         # 晉升大境界
                        action_screen.cultivation = 0               # 修為重置
                        print("🎉【逆天改命】你服下築基丹，真氣化液，成功破開天道屏障，晉升【築基期第1層】！")
                    else:
                        print("💥【突破失敗】你已達練氣期九層大圓滿！前方築基屏障堅不可摧，儲物袋中缺乏「築基丹」，無法破境！")
                else:
                    # 未遇到大境界瓶頸，交由境界系統執行日常修煉與小階突破（如1層升2層）
                    new_realm, new_cult, log_message = level_sys.train(
                        action_screen.realm,
                        action_screen.cultivation,
                        action_screen.spiritual_root
                    )
                    action_screen.realm = new_realm
                    action_screen.cultivation = new_cult
                    print(log_message)  

            # 2. 偵測點擊【前往煉丹】
            if action_screen.btn_alchemy.update():
                # 💡 暫時測試代碼：點擊前往煉丹時，先打賞玩家一顆築基丹，方便您測試突破機制
                item_sys.add_item("foundation_pill", 1)
                current_scene = "ALCHEMY"
                
            # 3. 偵測點擊【返回選單】
            if action_screen.btn_back.update():
                action_screen.show_archive_menu = False  # 離開前重置選單關閉
                current_scene = "MENU"

            # 4. 偵測點擊【天書玉簡】（切換多功能子選單）
            if action_screen.btn_archive.update():
                # 切換開關狀態
                action_screen.show_archive_menu = not action_screen.show_archive_menu
                if action_screen.show_archive_menu:
                    # 當子選單打開時，在「天書玉簡」按鈕的正上方動態建立 [存檔] 與 [讀取] 子按鈕
                    from Ui.Button import Button
                    # X 座標拆開，Y 座標往上移到 545
                    action_screen.btn_sub_save = Button(530, 545, 90, 45, "存檔", action_screen.font_path, 20)
                    action_screen.btn_sub_load = Button(620, 545, 90, 45, "讀取", action_screen.font_path, 20)

            # 5. 如果多功能選單是打開的，就額外偵測 [存檔] 與 [讀取] 的點擊
            if action_screen.show_archive_menu:
                # 偵測點擊【存檔】
                if action_screen.btn_sub_save and action_screen.btn_sub_save.update():
                    current_data = {
                        "name": action_screen.player_name,
                        "spiritual_root": action_screen.spiritual_root,
                        "cultivation": action_screen.cultivation,  # 手動存檔時記錄目前修為
                        "realm": action_screen.realm,              # 記錄目前境界
                        "inventory": item_sys.get_save_data(),     # 記錄目前背包
                    }
                    save_sys.save_game(current_data)  # 呼叫存檔系統寫入 JSON
                    action_screen.show_archive_menu = False  # 存完檔自動收起選單
                    print("【存檔】成功將當前修為與進度刻印至天書！")

                # 偵測點擊【讀取】
                if action_screen.btn_sub_load and action_screen.btn_sub_load.update():
                    data = save_sys.load_game()  # 呼叫存檔系統讀取 JSON
                    if data:
                        # 恢復玩家的基本動態資料
                        action_screen.enter_scene(data["name"], data["spiritual_root"])
                        # 恢復修為與境界數據
                        action_screen.cultivation = data.get("cultivation", 0)
                        action_screen.realm = data.get("realm", "凡人境界")
                        # 恢復儲物袋背包
                        item_sys.load_save_data(data.get("inventory", {}))
                        print("【讀取】成功破開時空，還原昔日修為與儲物袋！")
                    action_screen.show_archive_menu = False  # 讀取完自動收起選單



    # 螢幕顯示
    screen.fill(black)
    if action_screen:
        action_screen.draw(screen)

    pygame.display.flip()

pygame.quit()
sys.exit() 
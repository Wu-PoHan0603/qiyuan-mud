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
        # 主選單讀取時也支援恢復「儲物袋背包」
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
                    # 還原儲物袋背包數據
                    item_sys.load_save_data(data.get("inventory", {}))
                    
                    # 🌟【新增】讓一進遊戲的預設日誌顯示讀檔成功
                    scene["HOME"].add_log("【天道因果】成功堪破時空，載入前世仙緣進度。")
                    
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
            # 閉關修煉與「九層大圓滿卡關/消耗築基丹」機制綁定
            if action_screen.btn_train.update():
                # 判定：是否達到練氣九層瓶頸（根據 Level_system 練氣九層上限為 360）
                if "練氣期第9層" in action_screen.realm and action_screen.cultivation >= 360:
                    # 檢查儲物袋中有沒有築基丹
                    if item_sys.get_item_count("foundation_pill") > 0:
                        item_sys.remove_item("foundation_pill", 1)  # 消耗一顆築基丹
                        action_screen.realm = "築基期第1層"         # 晉升大境界
                        action_screen.cultivation = 0               # 修為重置
                        
                        # 🌟【修改點 1】突破大境界成功：同步推送到畫面日誌區
                        msg = "🎉【逆天改命】你服下築基丹，真氣化液，成功破開天道屏障，晉升【築基期第1層】！"
                        action_screen.add_log(msg)
                        print(msg)
                    else:
                        # 🌟【修改點 2】突破失敗卡關：同步推送到畫面日誌區
                        msg = "💥【突破失敗】你已達練氣期九層大圓滿！前方築基屏障堅不可摧，儲物袋中缺乏「築基丹」，無法破境！"
                        action_screen.add_log(msg)
                        print(msg)
                else:
                    # 未遇到大境界瓶頸，交由境界系統執行日常修煉與小階突破（如1層升2層）
                    new_realm, new_cult, log_message = level_sys.train(
                        action_screen.realm,
                        action_screen.cultivation,
                        action_screen.spiritual_root
                    )
                    action_screen.realm = new_realm
                    action_screen.cultivation = new_cult
                    
                    # 🌟【修改點 3】一般日常修煉：同步將修煉日誌推送到畫面日誌區
                    action_screen.add_log(log_message)
                    print(log_message)  
  

        elif current_scene == "HOME":
            # ════════════════════════════════════════════════════════════
            # 1. 基礎主導航按鈕偵測 (底部三大主按鈕)
            # ════════════════════════════════════════════════════════════
            
            # 偵測點擊【返回選單】
            if action_screen.btn_back.update():
                action_screen.show_archive_menu = False  # 離開前重置選單關閉
                current_scene = "MENU"

            # 偵測點擊【天書玉簡】（切換 11 大功能子選單的開關）
            if action_screen.btn_archive.update():
                action_screen.show_archive_menu = not action_screen.show_archive_menu

            # ════════════════════════════════════════════════════════════
            # 2. 依據天書選單【開啟 / 關閉】狀態進行分流偵測
            # ════════════════════════════════════════════════════════════
            if action_screen.show_archive_menu:
                # 🌟【天書玉簡開啟】偵測 11 大功能子按鈕的點擊事件
                
                # 1️⃣ 👉 偵測點擊【修士資訊】
                if action_screen.sub_buttons["STATUS"].update():
                    current_scene = "STATUS"
                    action_screen.show_archive_menu = False
                    action_screen.add_log("【天道窺探】展開修士法身，觀測根骨與命格。")
                    print("【洞府】前往修士資訊介面。")

                # 2️⃣ 👉 偵測點擊【儲物袋】
                elif action_screen.sub_buttons["BAG"].update():
                    current_scene = "BAG"
                    action_screen.show_archive_menu = False
                    action_screen.add_log("【儲物袋】神識探入袋中，清點修行資糧。")
                    print("【洞府】前往儲物袋背包介面。")

                # 3️⃣ 👉 偵測點擊【煉丹介面】
                elif action_screen.sub_buttons["ALCHEMY"].update():
                    # 💡 測試代碼：點擊前往煉丹時，先打賞玩家一顆築基丹，方便測試突破機制
                    item_sys.add_item("foundation_pill", 1)
                    current_scene = "ALCHEMY"
                    action_screen.show_archive_menu = False
                    action_screen.add_log("【丹道玄妙】引地心火，架紫金爐，準備煉製仙丹。")
                    print("【洞府】獲得測試築基丹*1，前往煉丹房。")

                # 4️⃣ 👉 偵測點擊【深層打坐】
                elif action_screen.sub_buttons["MEDITATE"].update():
                    current_scene = "MEDITATE"
                    action_screen.show_archive_menu = False
                    action_screen.add_log("【深層打坐】神游太虛，五心朝天，進入大定狀態。")
                    print("【洞府】進入深層打坐場景。")

                # 5️⃣ 👉 偵測點擊【極速修練】
                elif action_screen.sub_buttons["FAST_TRAIN"].update():
                    current_scene = "FAST_TRAIN"
                    action_screen.show_archive_menu = False
                    action_screen.add_log("【秘法逆天】燃燒壽元氣血，強行開啟百倍極速修煉！")
                    print("【洞府】進入極速修煉介面。")

                # 6️⃣ 👉 偵測點擊【探索秘境】
                elif action_screen.sub_buttons["EXPLORE"].update():
                    current_scene = "EXPLORE"
                    action_screen.show_archive_menu = False
                    action_screen.add_log("【尋仙問道】遁光飛出洞府，前往九幽秘境尋寶。")
                    print("【洞府】前往秘境探索。")

                # 7️⃣ 👉 偵測點擊【世界BOSS】
                elif action_screen.sub_buttons["BOSS"].update():
                    current_scene = "BOSS"
                    action_screen.show_archive_menu = False
                    action_screen.add_log("【神魔降世】遠方傳來洪荒巨獸怒吼，諸多大能正前往圍剿！")
                    print("【洞府】前往世界BOSS討伐戰。")

                # 8️⃣ 👉 偵測點擊【萬寶商店】
                elif action_screen.sub_buttons["SHOP"].update():
                    current_scene = "SHOP"
                    action_screen.show_archive_menu = False
                    action_screen.add_log("【萬寶閣】琳琅滿目，奇珍異寶盡在此處。")
                    print("【洞府】進入萬寶商店。")

                # 9️⃣ 👉 偵測點擊【刻印存檔】
                elif action_screen.sub_buttons["SAVE_GAME"].update():
                    current_data = {
                        "name": action_screen.player_name,
                        "spiritual_root": action_screen.spiritual_root,
                        "cultivation": action_screen.cultivation,
                        "realm": action_screen.realm,
                        "inventory": item_sys.get_save_data(),
                    }
                    save_sys.save_game(current_data)
                    action_screen.show_archive_menu = False  # 存完檔自動收起選單
                    
                    save_msg = "✨【天書刻印】道友運轉本源神識，已將一身修為封入天書玉簡。"
                    action_screen.add_log(save_msg)
                    print(save_msg)

                # 🔟 👉 偵測點擊【讀取仙緣】
                elif action_screen.sub_buttons["LOAD_GAME"].update():
                    data = save_sys.load_game()
                    if data:
                        action_screen.enter_scene(data["name"], data["spiritual_root"])
                        action_screen.cultivation = data.get("cultivation", 0)
                        action_screen.realm = data.get("realm", "凡人境界")
                        item_sys.load_save_data(data.get("inventory", {}))
                        
                        load_msg = "🌌【時空迴溯】天書微光大盛！昔日不滅因果已盡數重現人間。"
                        action_screen.add_log(load_msg)
                        print(load_msg)
                    else:
                        fail_msg = "❌【讀取失敗】天書無字，世間尚未留下道友的前世痕跡。"
                        action_screen.add_log(fail_msg)
                        print(fail_msg)
                    action_screen.show_archive_menu = False  # 讀取完自動收起選單

                # 1️⃣1️⃣ 👉 偵測點擊【系統設置】
                elif action_screen.sub_buttons["SETTING"].update():
                    current_scene = "SETTING"
                    action_screen.show_archive_menu = False
                    action_screen.add_log("【天道律令】調整法眼視界與天地仙音（系統設置）。")
                    print("【洞府】進入系統設置選單。")

            else:
                # 🌟【天書玉簡關閉】才允許點擊【閉關修煉】主按鈕（防止空氣穿透點擊）
                if action_screen.btn_train.update():
                    # 判定：是否達到練氣九層瓶頸
                    if "練氣期第9層" in action_screen.realm and action_screen.cultivation >= 360:
                        if item_sys.get_item_count("foundation_pill") > 0:
                            item_sys.remove_item("foundation_pill", 1)
                            action_screen.realm = "築基期第1層"
                            action_screen.cultivation = 0
                            action_screen.add_log("【天道突破】你吞服了築基丹，體內靈力液化，成功晉升築基期！")
                        else:
                            action_screen.add_log("【仙途瓶頸】你已達練氣圓滿，缺少「築基丹」強行突破將道基受損！")
                    else:
                        # 正常修煉：增加修為
                        current_max = level_lookup.get_max_cultivation(action_screen.realm)
                        if action_screen.cultivation < current_max:
                            action_screen.cultivation += 10
                            action_screen.add_log("【閉關修煉】你運轉周天功法，吐納天地靈氣，修為有所精進。")
                        else:
                            action_screen.add_log("【修為瓶頸】修為已至當前境界圓滿，請尋求突破之法！")





    # 螢幕顯示
    screen.fill(black)
    if action_screen:
        action_screen.draw(screen)

    pygame.display.flip()

pygame.quit()
sys.exit() 
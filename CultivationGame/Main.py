# Main.py
import os
import sys

import pygame

from SceneManager import SceneManager
from Scenes.Alchemy import AlchemyScene
from Scenes.Bag import BagScene
from Scenes.Battle import BattleScene
from Scenes.Create import CreateScene
from Scenes.Home import HomeScene
from Scenes.Menu import MenuScene
from Scenes.Shop import ShopScene
from Scenes.Status import StatusScene
from Scenes.Settings import SettingsScene
from Objects.DebugState import DebugState
from Systems.Item_system import ItemSystem
from Systems.Save_system import SaveSystem
from Systems.debug_system import DebugSystem
from Systems.settings_system import SettingsSystem
from Systems.data_reload_system import DataReloadSystem
from Systems.asset_manager import AssetManager
from Systems.audio_manager import AudioManager
from Systems.error_logger import ErrorLogger
from Ui.DebugOverlay import DebugOverlay


FPS = 60
WIDTH = 1000
HEIGHT = 700
BLACK = (0, 0, 0)


def load_background(base_dir):
    path = os.path.join(
        base_dir,
        "Assets",
        "Background",
        "Background.png",
    )

    try:
        image = pygame.image.load(path).convert()
        image = pygame.transform.scale(
            image,
            (WIDTH, HEIGHT),
        )
        image.set_alpha(160)
        return image
    except (pygame.error, FileNotFoundError):
        fallback = pygame.Surface((WIDTH, HEIGHT))
        fallback.fill((15, 20, 30))
        return fallback


def main():
    pygame.init()

    base_dir = os.path.dirname(os.path.abspath(__file__))
    error_logger = ErrorLogger(base_dir)
    sys.excepthook = error_logger.log_exception

    settings_system = SettingsSystem()
    game_settings = settings_system.load()
    if pygame.mixer.get_init():
        pygame.mixer.music.set_volume(game_settings.master_volume / 100)
    display_flags = pygame.FULLSCREEN if game_settings.fullscreen else 0
    screen = pygame.display.set_mode((WIDTH, HEIGHT), display_flags)
    pygame.display.set_caption("修仙世界")
    clock = pygame.time.Clock()

    font_path = os.path.join(
        base_dir,
        "Font",
        "LXGWWenKai-Medium.ttf",
    )

    save_system = SaveSystem()
    item_system = ItemSystem()
    data_reload_system = DataReloadSystem()
    asset_manager = AssetManager(base_dir, (WIDTH, HEIGHT))
    asset_manager.load_all()
    audio_manager = AudioManager(base_dir, game_settings.master_volume)
    audio_manager.validate_all()
    debug_state = DebugState()
    debug_system = DebugSystem()
    debug_overlay = DebugOverlay(font_path, debug_system)

    menu_scene = MenuScene(
        WIDTH,
        HEIGHT,
        font_path,
        asset_manager.get_background("MENU"),
    )
    create_scene = CreateScene(
        WIDTH,
        HEIGHT,
        font_path,
    )
    create_scene.set_background(asset_manager.get_background("CREATE"), 85)
    home_scene = HomeScene(
        WIDTH,
        HEIGHT,
        font_path,
        save_system,
        item_system,
        audio_manager=audio_manager,
    )
    home_scene.set_background(asset_manager.get_background("HOME"), 125)
    alchemy_scene = AlchemyScene(
        WIDTH,
        HEIGHT,
        font_path,
        item_system,
        player_provider=lambda: home_scene.player,
    )
    alchemy_scene.set_background(asset_manager.get_background("ALCHEMY"), 105)
    bag_scene = BagScene(
        WIDTH,
        HEIGHT,
        font_path,
        item_system,
        home_scene,
    )
    bag_scene.set_background(asset_manager.get_background("BAG"), 130)
    shop_scene = ShopScene(
        WIDTH, HEIGHT, font_path, item_system,
        lambda: home_scene.player,
    )
    shop_scene.set_background(asset_manager.get_background("SHOP"), 105)
    battle_scene = BattleScene(
        WIDTH, HEIGHT, font_path, item_system,
        lambda: home_scene.player,
        background_provider=asset_manager.get_background,
    )
    status_scene = StatusScene(
        WIDTH,
        HEIGHT,
        font_path,
        lambda: home_scene.player,
        home_scene.level_system,
    )
    status_scene.set_background(asset_manager.get_background("STATUS"), 135)
    settings_scene = SettingsScene(
        WIDTH,
        HEIGHT,
        font_path,
        settings_system,
        game_settings,
        audio_manager,
    )
    settings_scene.set_background(asset_manager.get_background("SETTINGS"), 150)

    manager = SceneManager(audio_manager)
    manager.add_scene("MENU", menu_scene)
    manager.add_scene("CREATE", create_scene)
    manager.add_scene("HOME", home_scene)
    manager.add_scene("ALCHEMY", alchemy_scene)
    manager.add_scene("BAG", bag_scene)
    manager.add_scene("SHOP", shop_scene)
    manager.add_scene("BATTLE", battle_scene)
    manager.add_scene("STATUS", status_scene)
    manager.add_scene("SETTINGS", settings_scene)
    manager.change_scene("MENU")

    running = True

    while running:
        clock.tick(game_settings.fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                continue

            if event.type == pygame.KEYDOWN and event.key == pygame.K_F1:
                debug_system.toggle(debug_state)
                home_scene.add_log(debug_state.last_message)
                continue

            if event.type == pygame.KEYDOWN and event.key == pygame.K_F2:
                image_ok, image_message = asset_manager.reload_all()
                audio_ok, audio_message = audio_manager.reload()
                if image_ok:
                    menu_scene.background = asset_manager.get_background("MENU")
                    create_scene.set_background(asset_manager.get_background("CREATE"), 85)
                    home_scene.set_background(asset_manager.get_background("HOME"), 125)
                    alchemy_scene.set_background(asset_manager.get_background("ALCHEMY"), 105)
                    bag_scene.set_background(asset_manager.get_background("BAG"), 130)
                    shop_scene.set_background(asset_manager.get_background("SHOP"), 105)
                    status_scene.set_background(asset_manager.get_background("STATUS"), 135)
                    settings_scene.set_background(asset_manager.get_background("SETTINGS"), 150)
                    battle_key = (
                        "BATTLE_DEMON"
                        if home_scene.player.realm_index >= 4
                        else "BATTLE"
                    )
                    battle_scene.set_background(
                        asset_manager.get_background(battle_key), 90
                    )
                message = f"{image_message} {audio_message}"
                if not image_ok or not audio_ok:
                    message = "Asset reload incomplete: " + message
                debug_system.report(debug_state, message)
                home_scene.add_log(message)
                continue

            if event.type == pygame.KEYDOWN and event.key == pygame.K_F3:
                ok, bundle, message = data_reload_system.validate_all()
                if ok:
                    ok, message = data_reload_system.apply_all(
                        bundle,
                        item_system,
                        alchemy_scene.alchemy_system,
                        battle_scene.system,
                    )
                if ok:
                    alchemy_scene.recipes = alchemy_scene.alchemy_system.recipes
                home_scene.add_log(message)
                continue

            if event.type == pygame.KEYDOWN and event.key == pygame.K_F4:
                if manager.reload_current():
                    message = f"Scene reloaded: {manager.current_name}"
                else:
                    message = "No active scene to reload"
                debug_system.report(debug_state, message)
                home_scene.add_log(message)
                continue

            if event.type == pygame.KEYDOWN and event.key == pygame.K_F5:
                if not debug_state.enabled:
                    home_scene.add_log("Enable Debug mode with F1 first")
                    continue
                player = home_scene.prepare_player_for_save()
                if save_system.save_debug_game(player):
                    message = "Debug save written"
                else:
                    message = "Debug save failed"
                debug_system.report(debug_state, message)
                home_scene.add_log(message)
                continue

            if event.type == pygame.KEYDOWN and event.key == pygame.K_F6:
                if not debug_state.enabled:
                    home_scene.add_log("Enable Debug mode with F1 first")
                    continue
                player = save_system.load_debug_game()
                if player is None:
                    message = "Debug save not found or invalid"
                else:
                    home_scene.set_player(player)
                    manager.change_scene("HOME")
                    message = "Debug save loaded"
                debug_system.report(debug_state, message)
                home_scene.add_log(message)
                continue

            current_name = manager.current_name
            result = manager.handle_event(event)

            if result is None:
                continue

            if result == "QUIT":
                running = False

            elif result == "LOAD":
                player = save_system.load_game()

                if player is not None:
                    home_scene.set_player(player)
                    manager.change_scene("HOME")

            elif (
                current_name == "CREATE"
                and result == "HOME"
            ):
                player = create_scene.created_player

                if player is not None:
                    home_scene.set_player(player)
                    save_system.save_game(player)
                    manager.change_scene("HOME")

            elif manager.has_scene(result):
                manager.change_scene(result)

        manager.update()

        screen.fill(BLACK)
        manager.draw(screen)
        debug_overlay.draw(
            screen,
            debug_state,
            manager.current_name,
            home_scene.player,
            clock.get_fps(),
        )
        pygame.display.flip()

    audio_manager.stop()
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()

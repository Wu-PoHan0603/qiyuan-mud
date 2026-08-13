# Main.py
import os
import sys

import pygame

from SceneManager import SceneManager
from Scenes.Alchemy import AlchemyScene
from Scenes.Bag import BagScene
from Scenes.Create import CreateScene
from Scenes.Home import HomeScene
from Scenes.Menu import MenuScene
from Systems.Item_system import ItemSystem
from Systems.Save_system import SaveSystem


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

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("修仙世界")
    clock = pygame.time.Clock()

    base_dir = os.path.dirname(os.path.abspath(__file__))
    font_path = os.path.join(
        base_dir,
        "Font",
        "LXGWWenKai-Medium.ttf",
    )

    save_system = SaveSystem()
    item_system = ItemSystem()

    menu_scene = MenuScene(
        WIDTH,
        HEIGHT,
        font_path,
        load_background(base_dir),
    )
    create_scene = CreateScene(
        WIDTH,
        HEIGHT,
        font_path,
    )
    home_scene = HomeScene(
        WIDTH,
        HEIGHT,
        font_path,
        save_system,
        item_system,
    )
    alchemy_scene = AlchemyScene(
        WIDTH,
        HEIGHT,
        font_path,
        item_system,
    )
    bag_scene = BagScene(
        WIDTH,
        HEIGHT,
        font_path,
        item_system,
        home_scene,
    )

    manager = SceneManager()
    manager.add_scene("MENU", menu_scene)
    manager.add_scene("CREATE", create_scene)
    manager.add_scene("HOME", home_scene)
    manager.add_scene("ALCHEMY", alchemy_scene)
    manager.add_scene("BAG", bag_scene)
    manager.change_scene("MENU")

    running = True

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
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
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()

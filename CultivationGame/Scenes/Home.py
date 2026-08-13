# Scenes/Home.py
import pygame

from Objects.Player import Player
from Scenes.BaseScene import BaseScene
from Systems.cultivation_system import CultivationSystem
from Systems.exploration_system import ExplorationSystem
from Systems.fast_training_system import FastTrainingSystem
from Systems.Level_system import LevelSystem
from Systems.meditation_system import MeditationSystem
from Ui.ArchiveMenu import ArchiveMenu
from Ui.Button import Button
from Ui.visuals import draw_panel, draw_shadow_text


class HomeScene(BaseScene):
    def __init__(
        self,
        width,
        height,
        font_path,
        save_system=None,
        item_system=None,
        meditation_system=None,
        exploration_system=None,
        cultivation_system=None,
        fast_training_system=None,
        audio_manager=None,
    ):
        self.width = width
        self.height = height
        self.font_path = font_path
        self.save_system = save_system
        self.item_system = item_system
        self.level_system = LevelSystem()
        self.meditation_system = (
            meditation_system or MeditationSystem()
        )
        self.exploration_system = (
            exploration_system or ExplorationSystem()
        )
        self.cultivation_system = (
            cultivation_system or CultivationSystem()
        )
        self.fast_training_system = (
            fast_training_system or FastTrainingSystem()
        )
        self.audio_manager = audio_manager
        self.player = Player()

        button_y = 610
        self.btn_train = Button(
            100, button_y, 220, 50,
            "閉關修煉", font_path, 24
        )
        self.btn_archive = Button(
            390, button_y, 220, 50,
            "天書玉簡", font_path, 24
        )
        self.btn_quit = Button(
            680, button_y, 220, 50,
            "離開遊戲", font_path, 24
        )

        self.archive_menu = ArchiveMenu(
            width,
            height,
            font_path,
        )

        self.logs = [
            "【天道指引】修仙洞府已開闢。",
            "",
            "",
            "",
            "",
            "",
        ]

    def set_player(self, player):
        if not isinstance(player, Player):
            raise TypeError(
                "HomeScene.set_player() 需要 Player。"
            )

        self.player = player

        if self.item_system is not None:
            self.item_system.load_save_data(
                self.player.inventory
            )

    def enter(self):
        print("【場景】進入洞府")

    def exit(self):
        self.archive_menu.close()

    def add_log(self, text):
        max_chars = 24
        lines = [
            text[i:i + max_chars]
            for i in range(0, len(text), max_chars)
        ] or [""]

        for line in lines:
            self.logs.pop(0)
            self.logs.append(line)

    def handle_event(self, event):
        if self.btn_quit.is_clicked(event):
            return "QUIT"

        if self.btn_archive.is_clicked(event):
            self.archive_menu.toggle()
            return None

        if self.archive_menu.is_open:
            action = self.archive_menu.handle_event(event)

            if action == "SAVE_GAME":
                self._save_game()
                self.archive_menu.close()
                return None

            if action == "LOAD_GAME":
                self._load_game()
                self.archive_menu.close()
                return None

            if action == "ALCHEMY":
                self.archive_menu.close()
                return "ALCHEMY"

            if action == "BAG":
                self.archive_menu.close()
                return "BAG"

            if action == "STATUS":
                self.archive_menu.close()
                return "STATUS"

            if action == "SETTING":
                self.archive_menu.close()
                return "SETTINGS"

            if action == "MEDITATE":
                self._meditate()
                self.archive_menu.close()
                return None

            if action == "EXPLORE":
                self._explore()
                self.archive_menu.close()
                return None

            if action == "FAST_TRAIN":
                self._fast_train()
                self.archive_menu.close()
                return None

            if action == "SHOP":
                self.archive_menu.close()
                return "SHOP"

            if action == "BOSS":
                self.archive_menu.close()
                return "BATTLE"

            if action is not None:
                button = self.archive_menu.buttons[action]
                self.add_log(
                    f"【功能建置中】{button.text}尚未完成。"
                )
                self.archive_menu.close()

            return None

        if self.btn_train.is_clicked(event):
            self._train()

        return None

    def _train(self):
        handled, _, message = self.level_system.attempt_major_breakthrough(
            self.player,
            self.item_system,
        )
        if handled:
            self.add_log(message)
            return

        _, message = self.cultivation_system.cultivate(
            self.player,
            self.level_system,
        )

        self.add_log(message)

    def _meditate(self):
        if self.audio_manager is not None:
            self.audio_manager.play_scene("MEDITATE")
        _, _, message = self.meditation_system.meditate(
            self.player
        )
        self.add_log(message)

    def _fast_train(self):
        _, message = self.fast_training_system.train(
            self.player,
            self.level_system,
            self.cultivation_system,
        )
        self.add_log(message)

    def _explore(self):
        _, message = self.exploration_system.explore(
            self.player,
            self.item_system,
            self.level_system,
        )
        self.add_log(message)

    def _sync_inventory_to_player(self):
        if self.item_system is not None:
            self.player.inventory = (
                self.item_system.get_save_data()
            )
            self.player.spirit_stone = (
                self.player.inventory.get(
                    "spirit_stone",
                    self.player.spirit_stone,
                )
            )

    def prepare_player_for_save(self):
        """Synchronize system-owned inventory before a save operation."""
        self._sync_inventory_to_player()
        return self.player

    def _save_game(self):
        if self.save_system is None:
            self.add_log("【存檔失敗】系統未連接。")
            return

        self._sync_inventory_to_player()

        if self.save_system.save_game(self.player):
            self.add_log("【天書刻印】進度已保存。")

    def _load_game(self):
        if self.save_system is None:
            self.add_log("【讀取失敗】系統未連接。")
            return

        player = self.save_system.load_game()

        if player is None:
            self.add_log("【讀取失敗】沒有存檔。")
            return

        self.set_player(player)
        self.add_log("【時空迴溯】仙緣已恢復。")

    def update(self):
        self.btn_train.update()
        self.btn_archive.update()
        self.btn_quit.update()
        self.archive_menu.update()

    def draw_text(
        self,
        surface,
        text,
        size,
        x,
        y,
        color=(255, 255, 255),
    ):
        font = pygame.font.Font(self.font_path, size)
        draw_shadow_text(surface, font, text, color, (x, y), "midtop")

    def draw(self, screen):
        self.draw_background(screen, (20, 30, 25))

        self.draw_text(
            screen,
            "─── 洞府神仙宅，修仙歲月長 ───",
            36,
            self.width // 2,
            45,
            (140, 200, 180),
        )

        if not self.archive_menu.is_open:
            self._draw_home_panel(screen)

        self.archive_menu.draw(screen)

        self.btn_train.draw(screen)
        self.btn_archive.draw(screen)
        self.btn_quit.draw(screen)

    def _draw_home_panel(self, screen):
        draw_panel(screen, (50, 150, 400, 350), (20, 32, 28, 220), (120, 175, 135, 235), 2, 12)

        self.draw_text(
            screen,
            "【 修士玉牌 】",
            26,
            250,
            170,
            (200, 220, 180),
        )
        self.draw_text(
            screen,
            f"名諱：{self.player.name}",
            22,
            250,
            230,
        )
        self.draw_text(
            screen,
            f"靈根：{self.player.spiritual_root}屬性",
            22,
            250,
            280,
            (120, 220, 160),
        )
        self.draw_text(
            screen,
            f"境界：{self.player.realm}",
            22,
            250,
            330,
            (230, 180, 100),
        )

        max_cultivation = (
            self.level_system.get_max_cultivation(
                self.player.realm
            )
        )

        self.draw_text(
            screen,
            "【 當前修為累積 】",
            24,
            700,
            180,
        )
        self.draw_text(
            screen,
            (
                f"{self.player.cultivation} "
                f"/ {max_cultivation} 點"
            ),
            28,
            700,
            220,
        )

        log_box = pygame.Rect(510, 280, 440, 220)
        draw_panel(screen, log_box, (16, 22, 25, 225), (105, 145, 120, 230), 2, 10)

        self.draw_text(
            screen,
            "─── 洞府修煉日誌 ───",
            20,
            log_box.centerx,
            292,
            (130, 170, 150),
        )

        font = pygame.font.Font(self.font_path, 15)

        for index, log_text in enumerate(self.logs):
            draw_shadow_text(
                screen, font, log_text, (225, 225, 215),
                (528, 330 + index * 26), "topleft", offset=(1, 1)
            )

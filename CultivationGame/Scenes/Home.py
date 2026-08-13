# Scenes/Home.py
import pygame

from Objects.Player import Player
from Scenes.BaseScene import BaseScene
from Systems.Level_system import LevelSystem
from Ui.ArchiveMenu import ArchiveMenu
from Ui.Button import Button


class HomeScene(BaseScene):
    def __init__(
        self,
        width,
        height,
        font_path,
        save_system=None,
        item_system=None,
    ):
        self.width = width
        self.height = height
        self.font_path = font_path
        self.save_system = save_system
        self.item_system = item_system
        self.level_system = LevelSystem()
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
        # 練氣九層圓滿，嘗試使用築基丹
        if (
            self.player.realm == "練氣期第9層"
            and self.player.cultivation
            >= self.level_system.get_max_cultivation(
                self.player.realm
            )
        ):
            if self.item_system is None:
                self.add_log(
                    "【突破失敗】背包系統尚未連接。"
                )
                return

            pill_count = self.item_system.get_item_count(
                "foundation_pill"
            )

            if pill_count <= 0:
                self.add_log(
                    "【突破失敗】缺少築基丹，無法突破築基期。"
                )
                return

            removed = self.item_system.remove_item(
                "foundation_pill",
                1,
            )

            if removed:
                self.player.realm = "築基期第1層"
                self.player.cultivation = 0

                self.add_log(
                    "【突破成功】服下築基丹，成功晉升築基期第1層！"
                )

            return

        (
            self.player.realm,
            self.player.cultivation,
            message,
        ) = self.level_system.train(
            self.player.realm,
            self.player.cultivation,
            self.player.spiritual_root,
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
        rendered = font.render(text, True, color)
        rect = rendered.get_rect(midtop=(x, y))
        surface.blit(rendered, rect)

    def draw(self, screen):
        screen.fill((20, 30, 25))

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
        pygame.draw.rect(
            screen,
            (35, 45, 40),
            (50, 150, 400, 350),
        )
        pygame.draw.rect(
            screen,
            (100, 150, 120),
            (50, 150, 400, 350),
            2,
        )

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
        pygame.draw.rect(
            screen,
            (22, 28, 30),
            log_box,
        )
        pygame.draw.rect(
            screen,
            (100, 130, 110),
            log_box,
            1,
        )

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
            rendered = font.render(
                log_text,
                True,
                (220, 220, 210),
            )
            screen.blit(
                rendered,
                (528, 330 + index * 26),
            )

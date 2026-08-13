import unittest

import pygame

from Scenes.Bag import BagScene
from Scenes.Home import HomeScene
from Scenes.Shop import ShopScene
from Systems.Item_system import ItemSystem


class InventoryShopLayoutTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()
        pygame.display.set_mode((1, 1))

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    def setUp(self):
        self.items = ItemSystem()
        self.home = HomeScene(1000, 700, None, item_system=self.items)
        self.bag = BagScene(1000, 700, None, self.items, self.home)
        self.shop = ShopScene(
            1000, 700, None, self.items, lambda: self.home.player
        )

    def test_all_bag_items_stay_inside_panel_and_window(self):
        window = pygame.Rect(0, 0, 1000, 700)
        for button in self.bag.item_buttons.values():
            self.assertTrue(self.bag.items_panel.contains(button.rect))
            self.assertTrue(window.contains(button.rect))

    def test_all_shop_items_stay_inside_panel_and_window(self):
        window = pygame.Rect(0, 0, 1000, 700)
        for button in self.shop.item_buttons.values():
            self.assertTrue(self.shop.items_panel.contains(button.rect))
            self.assertTrue(window.contains(button.rect))

    def test_bag_item_buttons_do_not_overlap(self):
        buttons = list(self.bag.item_buttons.values())
        for index, button in enumerate(buttons):
            for other in buttons[index + 1:]:
                self.assertFalse(button.rect.colliderect(other.rect))

    def test_shop_item_buttons_do_not_overlap(self):
        buttons = list(self.shop.item_buttons.values())
        for index, button in enumerate(buttons):
            for other in buttons[index + 1:]:
                self.assertFalse(button.rect.colliderect(other.rect))

    def test_action_buttons_do_not_overlap_item_panels(self):
        for button in (
            self.bag.btn_use_gathering,
            self.bag.btn_back,
            self.shop.btn_buy,
            self.shop.btn_sell,
            self.shop.btn_back,
        ):
            panel = (
                self.bag.items_panel
                if button in (self.bag.btn_use_gathering, self.bag.btn_back)
                else self.shop.items_panel
            )
            self.assertFalse(panel.colliderect(button.rect))

    def test_bag_and_shop_draw_without_clipping_crash(self):
        screen = pygame.Surface((1000, 700))
        self.bag.update()
        self.bag.draw(screen)
        self.shop.update()
        self.shop.draw(screen)


if __name__ == "__main__":
    unittest.main()

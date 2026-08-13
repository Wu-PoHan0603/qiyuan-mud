import unittest

import pygame

from Objects.Player import Player
from Scenes.Home import HomeScene
from Systems.Item_system import ItemSystem
from Systems.meditation_system import MeditationSystem


class HealingMechanismTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()
        pygame.display.set_mode((1, 1))

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    def test_meditation_restores_hp_and_mp(self):
        values = iter((40, 20))
        player = Player(hp=50, mp=40)
        ok, mp_recovery, message = MeditationSystem(
            lambda low, high: next(values)
        ).meditate(player)
        self.assertTrue(ok)
        self.assertEqual((player.hp, player.mp), (70, 80))
        self.assertEqual(mp_recovery, 40)
        self.assertIn("氣血恢復 20", message)

    def test_healing_never_exceeds_max_hp_or_mp(self):
        player = Player(hp=95, mp=90)
        MeditationSystem(lambda low, high: high).meditate(player)
        self.assertEqual((player.hp, player.mp), (100, 100))

    def test_full_mp_still_allows_hp_recovery(self):
        player = Player(hp=60, mp=100)
        ok, mp_recovery, message = MeditationSystem(
            lambda low, high: 25
        ).meditate(player)
        self.assertTrue(ok)
        self.assertEqual((player.hp, player.mp), (85, 100))
        self.assertEqual(mp_recovery, 0)
        self.assertIn("氣血恢復 25", message)

    def test_full_hp_still_allows_mp_recovery(self):
        player = Player(hp=100, mp=60)
        ok, mp_recovery, _ = MeditationSystem(
            lambda low, high: 30
        ).meditate(player)
        self.assertTrue(ok)
        self.assertEqual((player.hp, player.mp), (100, 90))
        self.assertEqual(mp_recovery, 30)

    def test_full_hp_and_mp_does_nothing(self):
        player = Player(hp=100, mp=100)
        ok, amount, _ = MeditationSystem().meditate(player)
        self.assertFalse(ok)
        self.assertEqual(amount, 0)

    def test_invalid_hp_is_rejected_without_mutation(self):
        player = Player()
        player.hp = -1
        before_mp = player.mp
        ok, _, _ = MeditationSystem().meditate(player)
        self.assertFalse(ok)
        self.assertEqual((player.hp, player.mp), (-1, before_mp))

    def test_home_meditation_logs_healing_result(self):
        items = ItemSystem()
        home = HomeScene(
            1000,
            700,
            None,
            item_system=items,
            meditation_system=MeditationSystem(lambda low, high: 20),
        )
        home.player.hp = 50
        home.player.mp = 50
        home._meditate()
        self.assertEqual((home.player.hp, home.player.mp), (70, 70))
        self.assertTrue(any("氣血恢復" in line for line in home.logs))


if __name__ == "__main__":
    unittest.main()

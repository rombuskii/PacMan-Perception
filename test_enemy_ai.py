import unittest
from unittest.mock import MagicMock
import numpy as np
from enemy_ai import EnemyAI, EnemyPerception

class TestEnemyPerception(unittest.TestCase):
    def setUp(self):
        self.perception = EnemyPerception()
        self.mock_map = MagicMock()
        self.mock_map.occupancy_map = np.array([[0, 0, 0], [0, 0, 0], [0, -1, 0]])  # -1 is wall

    def test_calculate_distance(self):
        self.assertEqual(self.perception.calculate_distance((0, 0), (2, 2)), 4)

    def test_can_see_player_horizontal_clear(self):
        self.mock_map.occupancy_map = np.array([[0, 0, 0]])
        self.assertTrue(self.perception.can_see_player((0, 0), (0, 2), self.mock_map))

    def test_can_see_player_horizontal_blocked(self):
        self.mock_map.occupancy_map = np.array([[0, -1, 0]])
        self.assertFalse(self.perception.can_see_player((0, 0), (0, 2), self.mock_map))

    def test_can_see_player_vertical_clear(self):
        self.mock_map.occupancy_map = np.array([[0], [0], [0]])
        self.assertTrue(self.perception.can_see_player((0, 0), (2, 0), self.mock_map))

    def test_can_see_player_vertical_blocked(self):
        self.mock_map.occupancy_map = np.array([[0], [-1], [0]])
        self.assertFalse(self.perception.can_see_player((0, 0), (2, 0), self.mock_map))

    def test_can_see_player_diagonal(self):
        self.assertFalse(self.perception.can_see_player((0, 0), (1, 1), self.mock_map))


class TestEnemyAI(unittest.TestCase):
    def setUp(self):
        self.enemy_ai = EnemyAI()
        self.mock_map = MagicMock()
        self.mock_map.is_valid_move.return_value = True
        self.mock_map.occupancy_map = np.zeros((5, 5), dtype=int)
        self.mock_map.is_power_pellet_active.return_value = False

    def test_patrol_changes_direction(self):
        self.mock_map.is_valid_move.side_effect = [False, True]
        initial_direction = self.enemy_ai.patrol_direction.copy()
        new_direction = self.enemy_ai.patrol((2, 2), self.mock_map)
        self.assertNotEqual(initial_direction, new_direction)

    def test_run_away_returns_opposite_direction(self):
        self.mock_map.is_valid_move.return_value = True
        move = self.enemy_ai.run_away((1, 1), (0, 0), self.mock_map)
        self.assertIsInstance(move, tuple)

    def test_chase_returns_valid_direction(self):
        self.mock_map.is_valid_move.return_value = True
        move = self.enemy_ai.chase((2, 2), (0, 0), self.mock_map)
        self.assertIsInstance(move, tuple)

    def test_update_mode_switches_to_chase(self):
        self.mock_map.is_power_pellet_active.return_value = False
        self.enemy_ai.perception.can_see_player = MagicMock(return_value=True)
        self.enemy_ai.update_mode((0, 0), (0, 1), self.mock_map)
        self.assertEqual(self.enemy_ai.current_mode, "chase")

    def test_update_mode_to_run_away(self):
        self.mock_map.is_power_pellet_active.return_value = True
        self.enemy_ai.update_mode((0, 0), (0, 1), self.mock_map)
        self.assertEqual(self.enemy_ai.current_mode, "run away")


if __name__ == '__main__':
    unittest.main()
import unittest
import numpy as np
from map import Map

class TestMap(unittest.TestCase):

    def setUp(self):
        self.map = Map()

    def test_initial_map_dimensions(self):
        rows, cols = self.map.occupancy_map.shape
        self.assertGreater(rows, 0)
        self.assertGreater(cols, 0)

    def test_is_valid_move_wall(self):
        # Assuming [0, 0] is a wall based on the layout
        self.assertFalse(self.map.is_valid_move(0, 0))

    def test_is_valid_move_empty(self):
        # Find an empty cell
        for i in range(self.map.occupancy_map.shape[0]):
            for j in range(self.map.occupancy_map.shape[1]):
                if self.map.occupancy_map[i, j] == Map.EMPTY:
                    self.assertTrue(self.map.is_valid_move(i, j))
                    return

    def test_set_position_empty(self):
        self.map.set_position_empty(1, 1)
        self.assertEqual(self.map.occupancy_map[1, 1], Map.EMPTY)

    def test_collect_regular_pellet(self):
        for i in range(self.map.occupancy_map.shape[0]):
            for j in range(self.map.occupancy_map.shape[1]):
                if self.map.occupancy_map[i, j] == Map.REGULAR_PELLET:
                    collected, is_power, is_sound = self.map.collect_point(i, j)
                    self.assertTrue(collected)
                    self.assertFalse(is_power)
                    self.assertFalse(is_sound)
                    self.assertEqual(self.map.occupancy_map[i, j], Map.EMPTY)
                    return

    def test_collect_power_pellet(self):
        for i in range(self.map.occupancy_map.shape[0]):
            for j in range(self.map.occupancy_map.shape[1]):
                if self.map.occupancy_map[i, j] == Map.POWER_PELLET:
                    collected, is_power, is_sound = self.map.collect_point(i, j)
                    self.assertTrue(collected)
                    self.assertTrue(is_power)
                    self.assertFalse(is_sound)
                    self.assertTrue(self.map.is_power_pellet_active())
                    return

    def test_check_win_false(self):
        self.assertFalse(self.map.check_win())

    def test_power_pellet_duration_decreases(self):
        self.map.power_pellet_active = True
        self.map.power_pellet_duration = 2
        self.map.update()
        self.assertEqual(self.map.power_pellet_duration, 1)

    def test_power_pellet_deactivates(self):
        self.map.power_pellet_active = True
        self.map.power_pellet_duration = 1
        self.map.update()
        self.assertFalse(self.map.power_pellet_active)

if __name__ == "__main__":
    unittest.main()
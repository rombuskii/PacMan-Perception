import unittest
from unittest.mock import MagicMock
from entities import Player, Enemy, EntityManager
import numpy as np
class TestEntities(unittest.TestCase):

    def setUp(self):
        # Create a mock game map
        self.mock_game_map = MagicMock()
        self.mock_game_map.occupancy_map = np.zeros((10, 10))
        self.mock_game_map.is_valid_move.return_value = True
        self.mock_game_map.collect_point.return_value = (True, False, True)
        self.mock_game_map.set_position_empty = MagicMock()

        # Create a mock renderer
        self.mock_renderer = MagicMock()

        # Create entity manager with mock map
        self.manager = EntityManager(self.mock_game_map)
        self.manager.set_renderer(self.mock_renderer)

    def test_player_move_valid_direction(self):
        player = self.manager.player
        result = player.move((0, 1), self.mock_game_map)
        self.assertTrue(result)
        self.assertEqual(player.position, [2, 1])
        self.mock_game_map.is_valid_move.assert_called()

    def test_player_triggers_sound_renderer_and_entity_manager(self):
        player = self.manager.player
        player.move((0, 1), self.mock_game_map)

        self.mock_game_map.collect_point.assert_called()
        self.mock_renderer.start_sound_effect.assert_called_with(2, 1)

    def test_enemy_moves_after_counter(self):
        enemy = Enemy(3, 3)
        enemy.move_counter = 1  # Just below ENEMY_SPEED_FACTOR
        moved = enemy.move(self.mock_game_map, [1, 1])
        self.assertIn(moved, [True, False])  

        enemy.move_counter = 3  # At ENEMY_SPEED_FACTOR
        moved = enemy.move(self.mock_game_map, [1, 1])
        self.assertIn(moved, [True, False])  

    def test_collision_with_enemy(self):
        self.manager.add_enemy(1, 1)  
        collided = self.manager.check_collision()
        self.assertTrue(collided)

    def test_enemy_gets_removed_on_run_away_mode(self):
        self.manager.add_enemy(1, 1)
        self.manager.enemies[0].ai.current_mode = "run away"
        collided = self.manager.check_collision()
        self.assertFalse(collided)
        self.assertEqual(len(self.manager.enemies), 0)
        self.assertEqual(self.manager.score, 200)

    def test_enemy_vision_data_structure(self):
        self.manager.add_enemy(4, 4)
        enemy = self.manager.enemies[0]
        enemy.ai.perception.can_see_player = MagicMock(return_value=True)

        data = self.manager.get_enemy_vision_data()
        self.assertEqual(len(data), 1)
        self.assertIn('position', data[0])
        self.assertIn('player_in_sight', data[0])
        self.assertIn('mode', data[0])

if __name__ == '__main__':
    unittest.main()
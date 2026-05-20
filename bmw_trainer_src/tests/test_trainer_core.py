"""
Unit tests for TrainerCore class.
"""

import unittest
from unittest.mock import patch, MagicMock
from black_myth_wukong_trainer.trainer_core import TrainerCore


class TestTrainerCore(unittest.TestCase):
    """Test suite for TrainerCore."""

    def setUp(self):
        self.trainer = TrainerCore(process_name="test_game.exe")

    def test_initial_cheat_states(self):
        """All cheats should start disabled."""
        for cheat, state in self.trainer._active_cheats.items():
            self.assertFalse(state, f"Cheat {cheat} should be False initially")

    def test_toggle_cheat_valid(self):
        """Toggling a valid cheat should flip its state."""
        self.trainer.toggle_cheat("infinite_health")
        self.assertTrue(self.trainer.get_cheat_state("infinite_health"))
        self.trainer.toggle_cheat("infinite_health")
        self.assertFalse(self.trainer.get_cheat_state("infinite_health"))

    def test_toggle_cheat_invalid(self):
        """Toggling an invalid cheat should return False."""
        result = self.trainer.toggle_cheat("nonexistent")
        self.assertFalse(result)

    @patch("black_myth_wukong_trainer.trainer_core.psutil.process_iter")
    def test_attach_to_game_success(self, mock_process_iter):
        """Should attach when process is found."""
        mock_proc = MagicMock()
        mock_proc.info = {"name": "test_game.exe", "pid": 1234}
        mock_process_iter.return_value = [mock_proc]
        result = self.trainer.attach_to_game()
        self.assertTrue(result)
        self.assertIsNotNone(self.trainer.game_process)

    @patch("black_myth_wukong_trainer.trainer_core.psutil.process_iter")
    def test_attach_to_game_failure(self, mock_process_iter):
        """Should return False when process not found."""
        mock_process_iter.return_value = []
        result = self.trainer.attach_to_game()
        self.assertFalse(result)
        self.assertIsNone(self.trainer.game_process)

    def test_register_hotkey(self):
        """Registering a hotkey should add it internally."""
        def dummy_callback():
            pass
        self.trainer.register_hotkey("ctrl+1", dummy_callback, "Test")
        self.assertIn("ctrl+1", self.trainer._hotkeys)

    def test_cleanup(self):
        """Cleanup should clear all hotkeys."""
        self.trainer.register_hotkey("ctrl+1", lambda: None, "Test")
        self.trainer.cleanup()
        self.assertEqual(len(self.trainer._hotkeys), 0)


if __name__ == "__main__":
    unittest.main()

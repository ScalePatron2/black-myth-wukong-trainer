"""
Core trainer logic for Black Myth: Wukong.
Handles hotkey registration, toggling cheats, and process attachment.
"""

import psutil
import keyboard
import logging
from typing import Dict, Callable, Optional

logger = logging.getLogger(__name__)


class TrainerCore:
    """Main trainer class that manages cheat toggles and game process."""

    def __init__(self, process_name: str = "b1-Win64-Shipping.exe"):
        self.process_name = process_name
        self.game_process: Optional[psutil.Process] = None
        self._hotkeys: Dict[str, Callable] = {}
        self._active_cheats: Dict[str, bool] = {
            "infinite_health": False,
            "infinite_mana": False,
            "no_cooldown": False,
            "unlimited_stamina": False
        }

    def attach_to_game(self) -> bool:
        """Find and attach to the Black Myth: Wukong game process."""
        for proc in psutil.process_iter(["name", "pid"]):
            if proc.info["name"] == self.process_name:
                self.game_process = proc
                logger.info(f"Attached to process {proc.info['name']} (PID: {proc.info['pid']})")
                return True
        logger.warning(f"Process {self.process_name} not found")
        return False

    def register_hotkey(self, key: str, callback: Callable, description: str = "") -> None:
        """Register a global hotkey to trigger a callback."""
        if key in self._hotkeys:
            logger.warning(f"Hotkey {key} already registered, overwriting")
        keyboard.add_hotkey(key, callback)
        self._hotkeys[key] = callback
        logger.info(f"Registered hotkey '{key}' for {description}")

    def toggle_cheat(self, cheat_name: str) -> bool:
        """Toggle a cheat on/off by name."""
        if cheat_name not in self._active_cheats:
            logger.error(f"Unknown cheat: {cheat_name}")
            return False
        self._active_cheats[cheat_name] = not self._active_cheats[cheat_name]
        state = "enabled" if self._active_cheats[cheat_name] else "disabled"
        logger.info(f"Cheat '{cheat_name}' {state}")
        return True

    def get_cheat_state(self, cheat_name: str) -> Optional[bool]:
        """Get current state of a cheat."""
        return self._active_cheats.get(cheat_name)

    def cleanup(self) -> None:
        """Remove all hotkeys and clean up resources."""
        for key in self._hotkeys:
            keyboard.remove_hotkey(key)
        self._hotkeys.clear()
        logger.info("Trainer cleaned up")

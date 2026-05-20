# Black Myth: Wukong Trainer package
# Provides tools for memory scanning, hotkey binding, and game process management.

from .trainer_core import TrainerCore
from .memory_scanner import MemoryScanner

__all__ = ["TrainerCore", "MemoryScanner"]

"""
Memory scanner for reading/writing game memory values.
Uces OpenCV for optional pattern matching on screen, and ctypes for memory manipulation.
"""

import ctypes
import ctypes.wintypes
from typing import Optional, List, Tuple
import logging

logger = logging.getLogger(__name__)

# Windows API constants
PROCESS_ALL_ACCESS = 0x1F0FFF


class MemoryScanner:
    """Scans and modifies game memory for trainer features."""

    def __init__(self, pid: int):
        self.pid = pid
        self._handle: Optional[int] = None
        self._open_process()

    def _open_process(self) -> None:
        """Open the target process with full access."""
        kernel32 = ctypes.windll.kernel32
        self._handle = kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, self.pid)
        if not self._handle:
            raise RuntimeError(f"Failed to open process {self.pid}")
        logger.info(f"Opened process handle for PID {self.pid}")

    def read_int(self, address: int) -> Optional[int]:
        """Read a 4-byte integer from memory address."""
        if not self._handle:
            return None
        buffer = ctypes.c_int()
        bytes_read = ctypes.c_size_t()
        kernel32 = ctypes.windll.kernel32
        success = kernel32.ReadProcessMemory(
            self._handle,
            ctypes.c_void_p(address),
            ctypes.byref(buffer),
            ctypes.sizeof(buffer),
            ctypes.byref(bytes_read)
        )
        if success:
            return buffer.value
        logger.warning(f"Failed to read at address {hex(address)}")
        return None

    def write_int(self, address: int, value: int) -> bool:
        """Write a 4-byte integer to memory address."""
        if not self._handle:
            return False
        buffer = ctypes.c_int(value)
        bytes_written = ctypes.c_size_t()
        kernel32 = ctypes.windll.kernel32
        success = kernel32.WriteProcessMemory(
            self._handle,
            ctypes.c_void_p(address),
            ctypes.byref(buffer),
            ctypes.sizeof(buffer),
            ctypes.byref(bytes_written)
        )
        if success:
            logger.info(f"Wrote {value} to {hex(address)}")
            return True
        logger.warning(f"Failed to write at address {hex(address)}")
        return False

    def pattern_scan(self, pattern: bytes, start: int, end: int) -> List[int]:
        """Simple pattern scan (placeholder for advanced scanning).
        In a real trainer, this would use signature scanning.
        """
        # Placeholder: in practice, use a more sophisticated scan
        logger.info(f"Pattern scan requested from {hex(start)} to {hex(end)}")
        return []

    def close(self) -> None:
        """Close the process handle."""
        if self._handle:
            kernel32 = ctypes.windll.kernel32
            kernel32.CloseHandle(self._handle)
            self._handle = None
            logger.info("Process handle closed")

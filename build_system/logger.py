"""Logging utilities"""
import sys
from enum import Enum

class LogLevel(Enum):
    DEBUG = 0
    INFO = 1
    SUCCESS = 2
    WARNING = 3
    ERROR = 4

class Logger:
    """Simple logging utility"""
    
    COLORS = {
        LogLevel.DEBUG: '\033[36m',
        LogLevel.INFO: '\033[34m',
        LogLevel.SUCCESS: '\033[32m',
        LogLevel.WARNING: '\033[33m',
        LogLevel.ERROR: '\033[31m',
    }
    RESET = '\033[0m'
    BOLD = '\033[1m'
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
    
    def _log(self, level: LogLevel, message: str, prefix: str = ""):
        color = self.COLORS.get(level, '')
        emoji_map = {
            LogLevel.DEBUG: "🔍",
            LogLevel.INFO: "ℹ️ ",
            LogLevel.SUCCESS: "✅",
            LogLevel.WARNING: "⚠️ ",
            LogLevel.ERROR: "❌",
        }
        emoji = emoji_map.get(level, "")
        output = f"{color}{self.BOLD}{emoji} {message}{self.RESET}"
        if prefix:
            output = f"  {prefix}: {output}"
        print(output, file=sys.stderr if level == LogLevel.ERROR else sys.stdout)
    
    def debug(self, message: str, prefix: str = ""):
        if self.verbose:
            self._log(LogLevel.DEBUG, message, prefix)
    
    def info(self, message: str, prefix: str = ""):
        self._log(LogLevel.INFO, message, prefix)
    
    def success(self, message: str, prefix: str = ""):
        self._log(LogLevel.SUCCESS, message, prefix)
    
    def warning(self, message: str, prefix: str = ""):
        self._log(LogLevel.WARNING, message, prefix)
    
    def error(self, message: str, prefix: str = ""):
        self._log(LogLevel.ERROR, message, prefix)
    
    def step(self, number: int, title: str):
        """Log a step header"""
        print(f"\n{self.BOLD}═════════════════════════════════════{self.RESET}")
        print(f"{self.BOLD}STEP {number}: {title}{self.RESET}")
        print(f"{self.BOLD}═════════════════════════════════════{self.RESET}\n")

#!/usr/bin/env python3
"""
PyTools v2.0.0 - Core Utilities Module
Configuration, logging, and utility functions
"""

import os
import sys
import logging
import json
import yaml
from pathlib import Path
from typing import Optional, Dict, Any
from logging.handlers import RotatingFileHandler
from datetime import datetime


class Config:
    """Configuration manager for PyTools"""

    _instance = None
    _config: Dict[str, Any] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self.config_dir = self._get_config_dir()
        self.config_file = os.path.join(self.config_dir, "config.yaml")
        self.load_config()

    def _get_config_dir(self) -> str:
        """Get configuration directory based on platform"""
        if sys.platform == "win32":
            base = os.environ.get("APPDATA", os.path.expanduser("~"))
            config_dir = os.path.join(base, "PyTools")
        elif os.environ.get("PREFIX", "").startswith("/data/data/com.termux"):
            # Termux
            config_dir = os.path.join(
                os.environ.get("HOME", os.path.expanduser("~")), ".config", "pytools"
            )
        else:
            # Linux/macOS
            config_dir = os.path.join(
                os.environ.get("XDG_CONFIG_HOME", os.path.expanduser("~/.config")),
                "pytools",
            )

        os.makedirs(config_dir, exist_ok=True)
        return config_dir

    def load_config(self):
        """Load configuration from file"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    self._config = yaml.safe_load(f) or {}
            except Exception as e:
                print(f"Warning: Failed to load config: {e}")
                self._config = self._get_default_config()
        else:
            self._config = self._get_default_config()
            self.save_config()

    def save_config(self):
        """Save configuration to file"""
        try:
            with open(self.config_file, "w", encoding="utf-8") as f:
                yaml.safe_dump(self._config, f, default_flow_style=False)
        except Exception as e:
            print(f"Warning: Failed to save config: {e}")

    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration"""
        return {
            "version": "2.0.0",
            "theme": "cyberpunk",
            "language": "en",
            "auto_update": True,
            "log_level": "INFO",
            "max_log_size": 10485760,  # 10MB
            "max_log_backups": 5,
            "show_animations": True,
            "terminal_width": "auto",
            "downloads": {
                "video_path": "VideosDownloads",
                "audio_path": "AudiosDownloads",
                "general_path": "Downloads",
                "max_retries": 3,
                "timeout": 30,
            },
            "network": {
                "timeout": 10,
                "ping_count": 4,
                "traceroute_max_hops": 30,
            },
            "security": {
                "min_password_length": 12,
                "show_password": False,
            },
            "system": {
                "clear_screen": True,
                "confirm_dangerous": True,
            },
        }

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        keys = key.split(".")
        value = self._config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default
        return value

    def set(self, key: str, value: Any):
        """Set configuration value"""
        keys = key.split(".")
        config = self._config
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        config[keys[-1]] = value
        self.save_config()

    def reset(self):
        """Reset configuration to defaults"""
        self._config = self._get_default_config()
        self.save_config()


class Logger:
    """Logging manager for PyTools"""

    _instance = None
    _logger: Optional[logging.Logger] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self.config = Config()
        self.setup_logging()

    def setup_logging(self):
        """Setup logging configuration"""
        # Get log directory
        log_dir = self.config.config_dir
        log_file = os.path.join(log_dir, "pytools.log")

        # Get log level
        log_level_str = self.config.get("log_level", "INFO")
        log_level = getattr(logging, log_level_str.upper(), logging.INFO)

        # Get log rotation settings
        max_bytes = self.config.get("max_log_size", 10485760)
        backup_count = self.config.get("max_log_backups", 5)

        # Create logger
        self._logger = logging.getLogger("pytools")
        self._logger.setLevel(log_level)

        # Remove existing handlers
        self._logger.handlers.clear()

        # Create rotating file handler
        try:
            file_handler = RotatingFileHandler(
                log_file, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8"
            )
            file_formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
            file_handler.setFormatter(file_formatter)
            self._logger.addHandler(file_handler)
        except Exception as e:
            print(f"Warning: Failed to setup file logging: {e}")

        # Create console handler for errors only
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.ERROR)
        console_formatter = logging.Formatter("%(levelname)s: %(message)s")
        console_handler.setFormatter(console_formatter)
        self._logger.addHandler(console_handler)

    def get_logger(self) -> logging.Logger:
        """Get logger instance"""
        return self._logger

    def info(self, message: str):
        """Log info message"""
        self._logger.info(message)

    def error(self, message: str, exc_info: bool = False):
        """Log error message"""
        self._logger.error(message, exc_info=exc_info)

    def warning(self, message: str):
        """Log warning message"""
        self._logger.warning(message)

    def debug(self, message: str):
        """Log debug message"""
        self._logger.debug(message)


class Cache:
    """Simple cache manager"""

    def __init__(self):
        self.config = Config()
        self.cache_dir = os.path.join(self.config.config_dir, "cache")
        os.makedirs(self.cache_dir, exist_ok=True)
        self._memory_cache: Dict[str, Any] = {}

    def set(self, key: str, value: Any, persist: bool = False):
        """Set cache value"""
        self._memory_cache[key] = value
        if persist:
            cache_file = os.path.join(self.cache_dir, f"{key}.json")
            try:
                with open(cache_file, "w", encoding="utf-8") as f:
                    json.dump(value, f)
            except:
                pass

    def get(self, key: str, default: Any = None) -> Any:
        """Get cache value"""
        if key in self._memory_cache:
            return self._memory_cache[key]

        cache_file = os.path.join(self.cache_dir, f"{key}.json")
        if os.path.exists(cache_file):
            try:
                with open(cache_file, "r", encoding="utf-8") as f:
                    value = json.load(f)
                    self._memory_cache[key] = value
                    return value
            except:
                pass

        return default

    def clear(self, key: Optional[str] = None):
        """Clear cache"""
        if key:
            self._memory_cache.pop(key, None)
            cache_file = os.path.join(self.cache_dir, f"{key}.json")
            if os.path.exists(cache_file):
                try:
                    os.remove(cache_file)
                except:
                    pass
        else:
            self._memory_cache.clear()
            try:
                for file in os.listdir(self.cache_dir):
                    os.remove(os.path.join(self.cache_dir, file))
            except:
                pass


def setup_logging():
    """Initialize logging system"""
    logger = Logger()
    return logger.get_logger()


def get_config() -> Config:
    """Get config instance"""
    return Config()


def get_logger() -> logging.Logger:
    """Get logger instance"""
    return Logger().get_logger()


def get_cache() -> Cache:
    """Get cache instance"""
    return Cache()

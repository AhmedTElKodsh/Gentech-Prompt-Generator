"""Configuration management system."""

import os
import json
import threading
from dataclasses import dataclass, field, asdict
from typing import Optional, Dict, Any
from enum import Enum, auto

class NotificationLevel(Enum):
    """Notification importance levels."""
    DEBUG = auto()
    INFO = auto()
    WARNING = auto()
    ERROR = auto()
    CRITICAL = auto()

class ConfigValidationError(Exception):
    """Raised when configuration validation fails."""
    pass

@dataclass
class NotificationConfig:
    """Notification-related configuration."""
    default_level: str = "info"
    duration: int = 5000
    
    def validate(self):
        """Validate notification configuration."""
        valid_levels = ["debug", "info", "warning", "error", "critical"]
        if self.default_level not in valid_levels:
            raise ValueError(f"Invalid notification level: {self.default_level}")
        if self.duration < 0:
            raise ValueError("Notification duration cannot be negative")

@dataclass
class UIConfig:
    """UI-related configuration."""
    theme: str = "light"
    font_size: int = 14
    enable_animations: bool = True
    
    def validate(self):
        """Validate UI configuration."""
        valid_themes = ["light", "dark"]
        if self.theme not in valid_themes:
            raise ValueError(f"Invalid theme: {self.theme}")
        if not 8 <= self.font_size <= 72:
            raise ValueError("Font size must be between 8 and 72")

@dataclass
class AppConfig:
    """Main application configuration manager."""
    config_file: Optional[str] = None
    notification: NotificationConfig = field(default_factory=NotificationConfig)
    ui: UIConfig = field(default_factory=UIConfig)
    debug_mode: bool = False
    log_level: str = "INFO"
    cache_responses: bool = True
    cache_dir: str = ".cache"
    max_history_items: int = 100
    api_timeout: int = 30
    max_retries: int = 3
    version: str = "1.0"  # Added version field
    
    _lock: threading.Lock = field(default_factory=threading.Lock, init=False)
    
    def __post_init__(self):
        """Initialize after instance creation."""
        # Load from environment variables
        self._load_from_env()
        
        # Load from config file if specified
        if self.config_file and os.path.exists(self.config_file):
            self._load_from_file()
    
    def _load_from_env(self):
        """Load configuration from environment variables."""
        env_mapping = {
            "APP_NOTIFICATION_LEVEL": ("notification", "default_level"),
            "APP_NOTIFICATION_DURATION": ("notification", "duration", int),
            "APP_UI_THEME": ("ui", "theme"),
            "APP_UI_FONT_SIZE": ("ui", "font_size", int),
            "APP_UI_ENABLE_ANIMATIONS": ("ui", "enable_animations", lambda x: x.lower() == "true"),
            "DEBUG_MODE": ("debug_mode", None, lambda x: x.lower() == "true"),
            "LOG_LEVEL": ("log_level", None),
            "MAX_HISTORY_ITEMS": ("max_history_items", None, int),
            "API_TIMEOUT": ("api_timeout", None, int)
        }
        
        for env_var, mapping in env_mapping.items():
            value = os.environ.get(env_var)
            if value is not None:
                section, key = mapping[0], mapping[1]
                # Apply type conversion if specified
                if len(mapping) > 2 and mapping[2] is not None:
                    try:
                        value = mapping[2](value)
                    except (ValueError, TypeError) as e:
                        raise ConfigValidationError(f"Invalid value for {env_var}: {e}")
                
                if key is None:
                    # Direct attribute of AppConfig
                    setattr(self, section, value)
                else:
                    # Nested attribute
                    section_obj = getattr(self, section)
                    setattr(section_obj, key, value)
                    section_obj.validate()
    
    def _load_from_file(self):
        """Load configuration from file."""
        try:
            with self._lock:
                with open(self.config_file, 'r') as f:
                    data = json.load(f)
                
                # Handle version migration
                if "version" in data:
                    self._migrate_config(data)
                
                try:
                    self.update(data)
                except ValueError as e:
                    raise ConfigValidationError(f"Error validating config file data: {e}")
        except json.JSONDecodeError as e:
            raise ConfigValidationError(f"Invalid JSON in config file: {e}")
        except FileNotFoundError:
            # Silently use defaults if file not found
            pass
        except PermissionError as e:
            raise ConfigValidationError(f"Permission denied accessing config file: {e}")
        except Exception as e:
            raise ConfigValidationError(f"Error loading config file: {e}")
    
    def _migrate_config(self, data: Dict[str, Any]):
        """Migrate configuration from older versions."""
        config_version = data.get("version", "1.0")
        
        # Migration from version 1.0 to current
        if config_version == "1.0":
            # Example migration: 'level' to 'default_level'
            if "notification" in data and "level" in data["notification"]:
                data["notification"]["default_level"] = data["notification"].pop("level")
        
        data["version"] = self.version
    
    def update(self, updates: Dict[str, Any]):
        """Update configuration with new values."""
        with self._lock:
            for section, values in updates.items():
                if not hasattr(self, section):
                    raise ValueError(f"Invalid configuration section: {section}")
                
                section_obj = getattr(self, section)
                
                # If it's a dict, it's for a nested config class
                if isinstance(values, dict):
                    for key, value in values.items():
                        if not hasattr(section_obj, key):
                            raise ValueError(f"Invalid configuration key: {key} in section {section}")
                        try:
                            setattr(section_obj, key, value)
                        except (ValueError, TypeError) as e:
                            raise ConfigValidationError(f"Invalid value for {section}.{key}: {e}")
                    
                    # Validate after all updates to the section if it has validate method
                    if hasattr(section_obj, 'validate'):
                        section_obj.validate()
                else:
                    # Direct attribute update
                    try:
                        setattr(self, section, values)
                    except (ValueError, TypeError) as e:
                        raise ConfigValidationError(f"Invalid value for {section}: {e}")
    
    def save(self):
        """Save current configuration to file."""
        if not self.config_file:
            raise ConfigValidationError("No config file specified")
        
        with self._lock:
            try:
                data = self.to_dict()
                
                # Ensure directory exists
                os.makedirs(os.path.dirname(os.path.abspath(self.config_file)), exist_ok=True)
                
                # Write to temporary file first
                temp_file = f"{self.config_file}.tmp"
                with open(temp_file, 'w') as f:
                    json.dump(data, f, indent=2)
                
                # Rename temporary file to actual config file
                os.replace(temp_file, self.config_file)
            except PermissionError as e:
                raise ConfigValidationError(f"Permission denied saving config file: {e}")
            except Exception as e:
                raise ConfigValidationError(f"Error saving config file: {e}")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return {
            "version": self.version,
            "notification": asdict(self.notification),
            "ui": asdict(self.ui),
            "debug_mode": self.debug_mode,
            "log_level": self.log_level,
            "cache_responses": self.cache_responses,
            "cache_dir": self.cache_dir,
            "max_history_items": self.max_history_items,
            "api_timeout": self.api_timeout,
            "max_retries": self.max_retries
        }
    
    def reset_to_defaults(self):
        """Reset all configuration values to their defaults."""
        with self._lock:
            self.notification = NotificationConfig()
            self.ui = UIConfig()
            self.debug_mode = False
            self.log_level = "INFO"
            self.cache_responses = True
            self.cache_dir = ".cache"
            self.max_history_items = 100
            self.api_timeout = 30
            self.max_retries = 3

# Global instance with thread safety
_config_instance = None
_config_lock = threading.Lock()

def get_config(config_file: Optional[str] = None) -> AppConfig:
    """Get or create the global configuration instance.
    
    Args:
        config_file: Optional path to a configuration file.
        
    Returns:
        The global AppConfig instance.
    """
    global _config_instance
    with _config_lock:
        if _config_instance is None:
            _config_instance = AppConfig(config_file=config_file)
        elif config_file is not None and config_file != _config_instance.config_file:
            _config_instance = AppConfig(config_file=config_file)
    return _config_instance

def update_config(updates: Dict[str, Any]) -> None:
    """Update the global configuration instance.
    
    Args:
        updates: Dictionary of configuration updates.
    """
    config = get_config()
    config.update(updates)

def reset_config() -> None:
    """Reset the global configuration instance to defaults."""
    global _config_instance
    with _config_lock:
        _config_instance = None 
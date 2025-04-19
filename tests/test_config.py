"""Tests for the configuration management system."""

import os
import json
import pytest
import threading
import tempfile
from pathlib import Path
from promptgen.config import (
    AppConfig,
    NotificationConfig,
    UIConfig,
    get_config,
    update_config,
    reset_config,
    NotificationLevel,
    ConfigValidationError
)
from typing import Dict, Any

@pytest.fixture
def app_config():
    """Fixture to provide a fresh AppConfig instance for each test."""
    config = AppConfig()
    yield config
    # Reset config after each test
    config.reset_to_defaults()

def test_default_config(app_config):
    """Test that default configuration values are set correctly."""
    assert app_config.notification.default_level == "info"
    assert app_config.notification.duration == 5000
    assert app_config.ui.theme == "light"
    assert app_config.ui.font_size == 14
    assert app_config.ui.enable_animations is True

def test_environment_override(monkeypatch):
    """Test configuration overrides via environment variables."""
    env_vars = {
        "APP_NOTIFICATION_LEVEL": "warning",
        "APP_UI_THEME": "dark",
        "APP_UI_FONT_SIZE": "16",
        "DEBUG_MODE": "true",
        "LOG_LEVEL": "DEBUG",
        "MAX_HISTORY_ITEMS": "50",
        "API_TIMEOUT": "60"
    }
    
    for key, value in env_vars.items():
        monkeypatch.setenv(key, value)
    
    # Reset config to load new environment variables
    reset_config()
    config = get_config()
    
    # Test overridden values
    assert config.notification.default_level == "warning"
    assert config.ui.theme == "dark"
    assert config.ui.font_size == 16
    assert config.debug_mode is True
    assert config.log_level == "DEBUG"
    assert config.max_history_items == 50
    assert config.api_timeout == 60

    # Clean up
    for key in env_vars:
        monkeypatch.delenv(key)
    reset_config()

def test_environment_validation(monkeypatch):
    """Test validation of environment variable values."""
    # Invalid environment values should be caught during loading
    # We'll test the validation separately
    
    # Test with type conversion
    monkeypatch.setenv("APP_UI_FONT_SIZE", "abc")  # Not a number
    reset_config()
    config = get_config()
    assert config.ui.font_size == 14  # Should keep default
    monkeypatch.delenv("APP_UI_FONT_SIZE")
    
    # Test boolean conversion
    monkeypatch.setenv("DEBUG_MODE", "TRUE")
    reset_config()
    config = get_config()
    assert config.debug_mode is True
    monkeypatch.delenv("DEBUG_MODE")
    
    # Cleanup
    reset_config()

def test_update_config(app_config):
    """Test dynamic configuration updates."""
    updates = {
        "notification": {
            "default_level": "error",
            "duration": 3000
        },
        "ui": {
            "theme": "dark",
            "font_size": 18,
            "enable_animations": False
        }
    }
    
    app_config.update(updates)
    
    assert app_config.notification.default_level == "error"
    assert app_config.notification.duration == 3000
    assert app_config.ui.theme == "dark"
    assert app_config.ui.font_size == 18
    assert app_config.ui.enable_animations is False

def test_update_config_global():
    """Test the global update_config function."""
    reset_config()
    
    # Make changes using the global function
    update_config({
        "debug_mode": True,
        "log_level": "DEBUG",
        "notification": {"default_level": "warning"}
    })
    
    config = get_config()
    assert config.debug_mode is True
    assert config.log_level == "DEBUG"
    assert config.notification.default_level == "warning"
    
    # Reset for cleanup
    reset_config()

def test_invalid_config_update():
    """Test handling of invalid configuration updates."""
    config = get_config()
    
    # Test invalid section
    with pytest.raises(ValueError, match="Invalid configuration section"):
        config.update({"non_existent_section": {"key": "value"}})
    
    # Test invalid key in a valid section
    with pytest.raises(ValueError, match="Invalid configuration key"):
        config.update({"notification": {"non_existent_key": "value"}})
    
    # Reset for cleanup
    reset_config()

def test_notification_config(app_config):
    """Test notification configuration specifics."""
    # Test notification level hierarchy
    valid_levels = ["debug", "info", "warning", "error", "critical"]
    for level in valid_levels:
        app_config.notification.default_level = level
        assert app_config.notification.default_level == level
    
    # Test invalid level
    with pytest.raises(ValueError):
        app_config.notification.default_level = "invalid_level"
    
    # Test duration bounds
    app_config.notification.duration = 1000
    assert app_config.notification.duration == 1000
    
    with pytest.raises(ValueError):
        app_config.notification.duration = -1
    
    # Test notification level enum ordering
    assert NotificationLevel.DEBUG.value < NotificationLevel.INFO.value
    assert NotificationLevel.INFO.value < NotificationLevel.WARNING.value
    assert NotificationLevel.WARNING.value < NotificationLevel.ERROR.value
    assert NotificationLevel.ERROR.value < NotificationLevel.CRITICAL.value

def test_ui_config(app_config):
    """Test UI configuration options."""
    # Test theme options
    valid_themes = ["light", "dark", "system"]
    for theme in valid_themes:
        app_config.ui.theme = theme
        assert app_config.ui.theme == theme
    
    with pytest.raises(ValueError):
        app_config.ui.theme = "invalid_theme"
    
    # Test font size bounds
    app_config.ui.font_size = 20
    assert app_config.ui.font_size == 20
    
    with pytest.raises(ValueError):
        app_config.ui.font_size = 0
    
    # Test UI component states
    assert app_config.ui.sidebar_initial_state in ["expanded", "collapsed"]
    assert isinstance(app_config.ui.page_title, str)
    assert isinstance(app_config.ui.page_icon, str)
    assert isinstance(app_config.ui.enable_dark_mode, bool)

def test_config_persistence(tmp_path):
    """Test configuration persistence and reset functionality."""
    config_path = tmp_path / "config.json"
    config = AppConfig(config_file=str(config_path))
    
    # Modify and save configuration
    updates = {
        "notification": {"default_level": "warning"},
        "ui": {"theme": "dark"}
    }
    config.update(updates)
    config.save()
    
    # Create new instance to test loading
    new_config = AppConfig(config_file=str(config_path))
    assert new_config.notification.default_level == "warning"
    assert new_config.ui.theme == "dark"
    
    # Test reset
    new_config.reset_to_defaults()
    assert new_config.notification.default_level == "info"
    assert new_config.ui.theme == "light"

def test_config_file_error_handling(tmp_path):
    """Test error handling for configuration file operations."""
    # Test with invalid JSON
    config_path = tmp_path / "invalid_config.json"
    with open(config_path, 'w') as f:
        f.write("{invalid json")
    
    with pytest.raises(ConfigValidationError):
        AppConfig(config_file=str(config_path))
    
    # Test save without config file
    config = AppConfig()
    with pytest.raises(ConfigValidationError):
        config.save()
    
    # Test with non-existent file
    non_existent_path = tmp_path / "nonexistent.json"
    config = AppConfig(config_file=str(non_existent_path))
    assert config.notification.default_level == "info"  # Should use defaults

def test_get_config():
    """Test the get_config singleton function."""
    # Test that get_config returns the same instance
    config1 = get_config()
    config2 = get_config()
    assert config1 is config2
    
    # Test that reset_config creates a new instance
    reset_config()
    config3 = get_config()
    assert config1 is not config3
    
    # Test default values after reset
    config = get_config()
    assert config.debug_mode is False
    assert config.log_level == "INFO"
    assert config.cache_responses is True
    assert config.cache_dir == ".cache"
    assert config.max_history_items == 100
    assert config.api_timeout == 30
    assert config.max_retries == 3
    
    # Test that configuration updates persist across get_config calls
    config.debug_mode = True
    config.log_level = "DEBUG"
    
    another_config = get_config()
    assert another_config.debug_mode is True
    assert another_config.log_level == "DEBUG"
    
    # Reset for cleanup
    reset_config()

def test_config_with_file_path(tmp_path):
    """Test get_config with a file path parameter."""
    # Create config file with custom settings
    config_path = tmp_path / "custom_config.json"
    config_data = {
        "notification": {"default_level": "error"},
        "ui": {"theme": "dark", "font_size": 18},
        "debug_mode": True
    }
    
    with open(config_path, 'w') as f:
        json.dump(config_data, f)
    
    # Get config with the file path
    reset_config()  # Make sure we start fresh
    config = get_config(config_file=str(config_path))
    
    # Verify settings were loaded
    assert config.notification.default_level == "error"
    assert config.ui.theme == "dark"
    assert config.ui.font_size == 18
    assert config.debug_mode is True
    
    # Reset for cleanup
    reset_config() 

def test_concurrent_access():
    """Test concurrent access to configuration."""
    reset_config()
    num_threads = 10
    iterations = 100
    
    def modify_config():
        for _ in range(iterations):
            config = get_config()
            config.debug_mode = not config.debug_mode
            config.log_level = "DEBUG" if config.log_level == "INFO" else "INFO"
    
    threads = [threading.Thread(target=modify_config) for _ in range(num_threads)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    
    # Verify config is in a valid state after concurrent modifications
    config = get_config()
    assert isinstance(config.debug_mode, bool)
    assert config.log_level in ["DEBUG", "INFO"]
    reset_config()

def test_config_inheritance():
    """Test configuration inheritance and overrides."""
    class CustomNotificationConfig(NotificationConfig):
        def __init__(self):
            super().__init__()
            self.custom_field = "custom"
    
    class CustomAppConfig(AppConfig):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.notification = CustomNotificationConfig()
    
    config = CustomAppConfig()
    assert config.notification.custom_field == "custom"
    assert config.notification.default_level == "info"
    
    # Test that updates still work with custom config
    config.update({
        "notification": {
            "default_level": "warning"
        }
    })
    assert config.notification.default_level == "warning"
    assert config.notification.custom_field == "custom"

def test_config_file_permissions(tmp_path):
    """Test configuration file permission handling."""
    config_path = tmp_path / "readonly_config.json"
    
    # Create initial config
    config = AppConfig(config_file=str(config_path))
    config.save()
    
    # Make file read-only
    os.chmod(config_path, 0o444)
    
    try:
        # Attempt to save to read-only file
        config.debug_mode = True
        with pytest.raises(ConfigValidationError):
            config.save()
    finally:
        # Restore permissions for cleanup
        os.chmod(config_path, 0o644)

def test_config_versioning(tmp_path):
    """Test configuration versioning and migration."""
    config_path = tmp_path / "versioned_config.json"
    
    # Create a config file with old version format
    old_config = {
        "version": "1.0",
        "notification": {
            "level": "info",  # old format used 'level' instead of 'default_level'
            "duration": 5000
        },
        "ui": {
            "theme": "light",
            "font_size": 14
        }
    }
    
    with open(config_path, 'w') as f:
        json.dump(old_config, f)
    
    # Load config and verify migration
    config = AppConfig(config_file=str(config_path))
    assert config.notification.default_level == "info"  # Should migrate 'level' to 'default_level'
    assert config.notification.duration == 5000
    assert config.ui.theme == "light"

def test_config_backup_restore(tmp_path):
    """Test configuration backup and restore functionality."""
    config_path = tmp_path / "config.json"
    backup_path = tmp_path / "config.json.bak"
    
    # Create initial config
    config = AppConfig(config_file=str(config_path))
    config.notification.default_level = "warning"
    config.ui.theme = "dark"
    config.save()
    
    # Create backup
    with open(config_path, 'r') as src, open(backup_path, 'w') as dst:
        dst.write(src.read())
    
    # Modify config
    config.notification.default_level = "error"
    config.save()
    
    # Restore from backup
    with open(backup_path, 'r') as src, open(config_path, 'w') as dst:
        dst.write(src.read())
    
    # Load restored config
    restored_config = AppConfig(config_file=str(config_path))
    assert restored_config.notification.default_level == "warning"
    assert restored_config.ui.theme == "dark"

def test_config_export_import(tmp_path):
    """Test configuration export and import functionality."""
    # Create config with custom settings
    config = AppConfig()
    config.notification.default_level = "warning"
    config.ui.theme = "dark"
    config.debug_mode = True
    
    # Export to JSON
    export_path = tmp_path / "exported_config.json"
    with open(export_path, 'w') as f:
        json.dump(config.to_dict(), f)
    
    # Create new config and import settings
    imported_config = AppConfig()
    with open(export_path, 'r') as f:
        imported_data = json.load(f)
        imported_config.update(imported_data)
    
    # Verify imported settings
    assert imported_config.notification.default_level == "warning"
    assert imported_config.ui.theme == "dark"
    assert imported_config.debug_mode is True

def test_config_validation_edge_cases():
    """Test edge cases for configuration validation."""
    config = AppConfig()
    
    # Test empty string values
    with pytest.raises(ValueError):
        config.notification.default_level = ""
    
    # Test None values
    with pytest.raises(ValueError):
        config.notification.duration = None
    
    # Test negative numbers where not allowed
    with pytest.raises(ValueError):
        config.notification.duration = -1
    
    # Test extremely large numbers
    with pytest.raises(ValueError):
        config.ui.font_size = 1000000
    
    # Test invalid types
    with pytest.raises(TypeError):
        config.debug_mode = "not a boolean"
    
    with pytest.raises(TypeError):
        config.notification.duration = "not a number"
    
    # Test boundary values
    config.notification.duration = 0  # Should be allowed
    assert config.notification.duration == 0
    
    config.ui.font_size = 8  # Minimum allowed
    assert config.ui.font_size == 8
    
    config.ui.font_size = 72  # Maximum allowed
    assert config.ui.font_size == 72 
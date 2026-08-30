"""Tests for configuration management."""

from __future__ import annotations

import pytest
from pathlib import Path

from itinerpic.config import AppConfig, Config


class TestAppConfig:
    """Test AppConfig model."""

    def test_default_paths(self):
        """Test default path configuration."""
        config = AppConfig()
        assert config.project_root.exists()
        assert config.src_dir.exists()

    def test_custom_encoding(self):
        """Test custom encoding configuration."""
        config = AppConfig(encoding="ascii")
        assert config.encoding == "ascii"

    def test_template_engine_options(self):
        """Test template engine configuration."""
        config_jinja = AppConfig(template_engine="jinja2")
        assert config_jinja.template_engine == "jinja2"

        config_simple = AppConfig(template_engine="simple")
        assert config_simple.template_engine == "simple"

    def test_ensure_directories(self):
        """Test that directories are created."""
        config = AppConfig()
        config.ensure_directories()
        assert config.summaries_dir.exists()
        assert config.config_dir.exists()


class TestConfigSingleton:
    """Test Config singleton manager."""

    def test_singleton_instance(self):
        """Test that Config returns same instance."""
        Config.reset()
        config1 = Config.get()
        config2 = Config.get()
        assert config1 is config2

    def test_reset(self):
        """Test Config reset."""
        config1 = Config.get()
        Config.reset()
        config2 = Config.get()
        assert config1 is not config2

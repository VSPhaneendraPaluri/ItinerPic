"""Tests for generators."""

from __future__ import annotations

import pytest
import tempfile
from pathlib import Path

from itinerpic.config import AppConfig, Config
from itinerpic.generators import PlanGenerator


class TestPlanGenerator:
    """Test PlanGenerator."""

    def setup_method(self):
        """Setup test environment."""
        Config.reset()

    def test_output_filename(self):
        """Test output filename."""
        generator = PlanGenerator()
        assert generator.output_filename == "itinerpic_plan.md"

    def test_render_content(self):
        """Test that template renders."""
        generator = PlanGenerator()
        content = generator.render()
        assert "ItinerPic" in content
        assert "Detailed Project Plan" in content

    def test_generate_creates_file(self):
        """Test that generate creates output file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = AppConfig(summaries_dir=Path(tmpdir))
            generator = PlanGenerator(config=config)
            output_path = generator.generate()
            assert output_path.exists()
            assert output_path.read_text()

    def test_from_custom_data(self):
        """Test generator with custom data."""
        custom_data = {
            "title": "Custom Title",
            "overview": "Custom overview",
            "goals": ["Goal 1", "Goal 2"],
            "features": ["Feature 1"],
            "tech_stack": {},
            "architecture": "Custom arch",
            "data_model": "Custom model",
            "next_steps": ["Step 1"],
        }
        generator = PlanGenerator.from_data(custom_data)
        content = generator.render()
        assert "Custom Title" in content
        assert "Custom overview" in content
        assert "Goal 1" in content

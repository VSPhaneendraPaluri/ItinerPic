"""Tests for template management."""

from __future__ import annotations

import pytest

from itinerpic.templates import TemplateManager


class TestTemplateManager:
    """Test TemplateManager."""

    def test_simple_variable_replacement(self):
        """Test simple variable replacement."""
        manager = TemplateManager(engine="simple")
        template = "Hello {{ name }}"
        context = {"name": "World"}
        result = manager.render(template, context)
        assert result == "Hello World"

    def test_jinja2_availability(self):
        """Test that Jinja2 renderer works if available."""
        manager = TemplateManager(engine="jinja2")
        template = "Value: {{ value }}"
        context = {"value": 42}
        result = manager.render(template, context)
        assert "42" in result

    def test_list_rendering(self):
        """Test rendering of lists."""
        manager = TemplateManager(engine="simple")
        template = """Items:
{% for item in items %}- {{ item }}
{% endfor %}"""
        context = {"items": ["apple", "banana", "cherry"]}
        result = manager.render(template, context)
        assert "- apple" in result
        assert "- banana" in result
        assert "- cherry" in result

    def test_invalid_engine(self):
        """Test that invalid engine raises error."""
        with pytest.raises(ValueError):
            TemplateManager(engine="invalid_engine")

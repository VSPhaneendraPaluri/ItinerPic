"""Template management and rendering."""

from __future__ import annotations

import logging
import re
from abc import ABC, abstractmethod
from typing import Any, Dict

try:
    from jinja2 import Template
    JINJA2_AVAILABLE = True
except ImportError:
    JINJA2_AVAILABLE = False

logger = logging.getLogger(__name__)


class TemplateRenderer(ABC):
    """Abstract base class for template renderers."""

    @abstractmethod
    def render(self, template_str: str, context: Dict[str, Any]) -> str:
        """Render template with context."""
        pass


class Jinja2Renderer(TemplateRenderer):
    """Jinja2 template renderer."""

    def render(self, template_str: str, context: Dict[str, Any]) -> str:
        """
        Render template using Jinja2.

        Args:
            template_str: Template string
            context: Context dictionary

        Returns:
            Rendered content
        """
        if not JINJA2_AVAILABLE:
            raise RuntimeError("Jinja2 is not installed. Install with: pip install Jinja2")

        template = Template(template_str)
        return template.render(**context)


class SimpleRenderer(TemplateRenderer):
    """Simple fallback renderer (no Jinja2 required)."""

    @staticmethod
    def _resolve_value(context: Dict[str, Any], expression: str) -> Any:
        expression = expression.strip()
        if not expression:
            return ""

        if expression == "loop.index":
            return context.get("_loop_index", 0)

        if expression.startswith("loop."):
            loop_data = context.get("_loop_data") or {}
            return loop_data.get(expression.split(".", 1)[1], 0)

        current: Any = context
        for part in expression.split("."):
            if isinstance(current, dict):
                current = current.get(part)
            else:
                current = getattr(current, part, None)
            if current is None:
                break
        return current

    @classmethod
    def _render_with_scope(cls, template_str: str, context: Dict[str, Any]) -> str:
        def replace_var(match: re.Match[str]) -> str:
            expression = match.group(1).strip()
            value = cls._resolve_value(context, expression)
            return "" if value is None else str(value)

        content = template_str

        loop_pattern = re.compile(
            r"{%\s*for\s+(\w+)\s+in\s+([\w\.]+)\s*%}(.*?){%\s*endfor\s*%}",
            re.DOTALL,
        )
        while True:
            match = loop_pattern.search(content)
            if not match:
                break

            item_name, iterable_name, loop_body = match.groups()
            iterable = cls._resolve_value(context, iterable_name)
            if not isinstance(iterable, (list, tuple)):
                iterable = []

            rendered = []
            for index, item in enumerate(iterable, start=1):
                local_context = dict(context)
                local_context[item_name] = item
                local_context["_loop_index"] = index
                local_context["_loop_data"] = {"index": index, "length": len(iterable)}
                rendered.append(cls._render_with_scope(loop_body, local_context))

            content = content[: match.start()] + "".join(rendered) + content[match.end() :]

        content = re.sub(r"{{\s*([^{}]+?)\s*}}", replace_var, content)
        return content

    def render(self, template_str: str, context: Dict[str, Any]) -> str:
        """
        Render template using simple string replacement.

        Args:
            template_str: Template string
            context: Context dictionary

        Returns:
            Rendered content

        Note:
            Only supports {{ variable }} syntax and basic {% for %} loops.
        """
        content = self._render_with_scope(template_str, context)
        logger.debug("Used simple template rendering (Jinja2 not available)")
        return content


class TemplateManager:
    """Manages template selection and rendering."""

    def __init__(self, engine: str = "jinja2"):
        """
        Initialize template manager.

        Args:
            engine: Template engine to use ('jinja2' or 'simple')
        """
        self.engine = engine
        self._renderer = self._get_renderer()

    def _get_renderer(self) -> TemplateRenderer:
        """
        Get appropriate renderer based on engine selection.

        Returns:
            TemplateRenderer instance
        """
        if self.engine.lower() == "jinja2":
            if JINJA2_AVAILABLE:
                logger.info("Using Jinja2 template renderer")
                return Jinja2Renderer()
            else:
                logger.warning("Jinja2 not available, falling back to simple renderer")
                return SimpleRenderer()
        elif self.engine.lower() == "simple":
            logger.info("Using simple template renderer")
            return SimpleRenderer()
        else:
            raise ValueError(f"Unknown template engine: {self.engine}")

    def render(self, template_str: str, context: Dict[str, Any]) -> str:
        """
        Render template with context.

        Args:
            template_str: Template string
            context: Context dictionary

        Returns:
            Rendered content
        """
        return self._renderer.render(template_str, context)

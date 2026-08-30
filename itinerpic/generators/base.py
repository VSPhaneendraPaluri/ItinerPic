"""Base generator class."""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict

from ..config import Config
from ..templates import TemplateManager
from ..utils.io import write_file

logger = logging.getLogger(__name__)


class BaseGenerator(ABC):
    """
    Abstract base class for all generators.

    Provides common functionality for rendering and writing output files.
    """

    def __init__(self, config: Config | None = None, template_engine: str = "jinja2"):
        """
        Initialize generator.

        Args:
            config: Application configuration
            template_engine: Template engine to use
        """
        self.config = config or Config.get()
        self.template_manager = TemplateManager(engine=template_engine)

    @property
    @abstractmethod
    def output_filename(self) -> str:
        """Get the output filename for this generator."""
        pass

    @property
    def output_path(self) -> Path:
        """Get the full output path."""
        return self.config.summaries_dir / self.output_filename

    @abstractmethod
    def get_template(self) -> str:
        """Get the template string."""
        pass

    @abstractmethod
    def get_context(self) -> Dict[str, Any]:
        """Get the context dictionary for rendering."""
        pass

    def render(self) -> str:
        """
        Render the template with context.

        Returns:
            Rendered content
        """
        template = self.get_template()
        context = self.get_context()
        content = self.template_manager.render(template, context)
        logger.debug(f"Rendered template for {self.output_filename}")
        return content

    def generate(self) -> Path:
        """
        Generate and write output file.

        Returns:
            Path to generated file
        """
        content = self.render()
        write_file(
            self.output_path,
            content,
            encoding=self.config.encoding,
            overwrite=self.config.overwrite,
        )
        logger.info(f"Generated {self.output_filename}")
        return self.output_path

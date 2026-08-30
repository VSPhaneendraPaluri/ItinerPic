"""ItinerPic web application package."""

__version__ = "1.0.0"
__author__ = "ItinerPic Team"

from .config import Config
from .generators import SiteGenerator

__all__ = ["Config", "SiteGenerator", "__version__", "__author__"]

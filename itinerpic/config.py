"""Application configuration for the ItinerPic website."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

try:
    from dotenv import load_dotenv

    _DOTENV_AVAILABLE = True
except ImportError:
    _DOTENV_AVAILABLE = False


class AppConfig:
    """Central configuration for the travel app."""

    def __init__(
        self,
        project_root: Optional[Path] = None,
        src_dir: Optional[Path] = None,
        templates_dir: Optional[Path] = None,
        static_dir: Optional[Path] = None,
        dist_dir: Optional[Path] = None,
        summaries_dir: Optional[Path] = None,
        config_dir: Optional[Path] = None,
        app_name: str = "ItinerPic",
        app_title: str = "ItinerPic | Travel planning, beautifully",
        template_engine: str = "jinja2",
        debug: bool = False,
        host: str = "0.0.0.0",
        port: int = 8000,
        encoding: str = "utf-8",
        overwrite: bool = True,
        secret_key: Optional[str] = None,
    ):
        base_dir = Path(__file__).resolve().parent.parent
        self.project_root = project_root or base_dir
        # package-based layout: code lives under ./itinerpic
        self.src_dir = src_dir or (base_dir / "itinerpic")
        self.templates_dir = templates_dir or (base_dir / "itinerpic" / "templates")
        self.static_dir = static_dir or (base_dir / "itinerpic" / "static")
        self.dist_dir = dist_dir or (base_dir / "dist")
        self.summaries_dir = summaries_dir or (base_dir / "summaries")
        self.config_dir = config_dir or (base_dir / "config")

        self.app_name = app_name
        self.app_title = app_title
        self.template_engine = template_engine
        self.debug = debug
        self.host = host
        self.port = port
        self.encoding = encoding
        self.overwrite = overwrite
        self.secret_key = secret_key or "dev-itinerpic-secret-key"

    def ensure_directories(self) -> None:
        self.templates_dir.mkdir(parents=True, exist_ok=True)
        self.static_dir.mkdir(parents=True, exist_ok=True)
        self.dist_dir.mkdir(parents=True, exist_ok=True)
        self.summaries_dir.mkdir(parents=True, exist_ok=True)
        self.config_dir.mkdir(parents=True, exist_ok=True)


class Config:
    """Singleton configuration manager."""

    _instance: Optional[AppConfig] = None

    @classmethod
    def get(cls) -> AppConfig:
        if cls._instance is None:
            if _DOTENV_AVAILABLE:
                load_dotenv()

            cls._instance = AppConfig(
                app_name=os.getenv("APP_NAME", "ItinerPic"),
                app_title=os.getenv("APP_TITLE", "ItinerPic | Travel planning, beautifully"),
                template_engine=os.getenv("TEMPLATE_ENGINE", "jinja2"),
                debug=os.getenv("DEBUG", "false").lower() == "true",
                host=os.getenv("HOST", "0.0.0.0"),
                port=int(os.getenv("PORT", "8000")),
                overwrite=os.getenv("OVERWRITE", "true").lower() == "true",
                secret_key=os.getenv("SECRET_KEY", "dev-itinerpic-secret-key"),
            )
            cls._instance.ensure_directories()
        return cls._instance

    @classmethod
    def reset(cls) -> None:
        cls._instance = None

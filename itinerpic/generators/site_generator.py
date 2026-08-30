from __future__ import annotations

from typing import Any, Dict

from .base import BaseGenerator
from ..utils.io import read_file


def get_homepage_data() -> Dict[str, Any]:
    def static_url(endpoint: str = "static", **kwargs: Any) -> str:
        if endpoint == "static" and "filename" in kwargs:
            return f"/static/{kwargs['filename']}"
        return "/static/styles.css"

    return {
        "brand": "ItinerPic",
        "tagline": "Plan the trip you actually want to take.",
        "subtitle": (
            "Turn ideas, local recommendations, and photo memories into a destination-aware "
            "itinerary that feels effortless to follow."
        ),
        "url_for": static_url,
        "stats": [
            {"value": "4.9/5", "label": "traveler rating"},
            {"value": "24K+", "label": "plans created"},
            {"value": "18", "label": "countries mapped"},
        ],
        "highlights": [
            "AI-assisted route matching",
            "Photo-first trip memory boards",
            "Collaborative itinerary planning",
        ],
        "destinations": [
            {
                "name": "Kyoto",
                "country": "Japan",
                "days": "4 days",
                "accent": "#f3c98b",
                "description": "Temple walks, ramen nights, and quiet mornings in Gion.",
            },
            {
                "name": "Amalfi",
                "country": "Italy",
                "days": "5 days",
                "accent": "#8ed7d1",
                "description": "Coastal drives, lemon groves, and sunset dinners by the sea.",
            },
            {
                "name": "Bali",
                "country": "Indonesia",
                "days": "6 days",
                "accent": "#d09ce9",
                "description": "Wellness retreats, jungle cafes, and beachside mornings.",
            },
            {
                "name": "Cape Town",
                "country": "South Africa",
                "days": "5 days",
                "accent": "#7abaf5",
                "description": "Mountain drives, harbor food markets, and coastal viewpoints.",
            },
        ],
        "steps": [
            {
                "title": "Capture the vibe",
                "content": "Drop in your dream pace, places, and travel style to shape the plan.",
            },
            {
                "title": "Map the route",
                "content": "Arrange days, move times, neighborhoods, and memorable stops naturally.",
            },
            {
                "title": "Travel beautifully",
                "content": "Share the final plan with friends and turn every moment into a story.",
            },
        ],
        "trip_card": {
            "title": "Your next adventure",
            "meta": "Add a trip to start planning",
            "snapshot": [
                {"label": "Days", "value": "—"},
                {"label": "Budget", "value": "₹0"},
                {"label": "Mood", "value": "custom"},
            ],
        },
    }


class SiteGenerator(BaseGenerator):
    @property
    def output_filename(self) -> str:
        return "index.html"

    @property
    def output_path(self):
        return self.config.dist_dir / self.output_filename

    def get_template(self) -> str:
        template_path = self.config.templates_dir / "index.html"
        return read_file(template_path)

    def get_context(self) -> Dict[str, Any]:
        return get_homepage_data()

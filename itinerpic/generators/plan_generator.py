"""Plan generator for ItinerPic project documentation."""

from __future__ import annotations

import logging
from typing import Any, Dict

from .base import BaseGenerator

logger = logging.getLogger(__name__)


# Plan data structure - can be moved to config/yaml for scalability
PLAN_DATA = {
    "title": "ItinerPic — Detailed Project Plan",
    "overview": (
        "ItinerPic is a modern travel planning platform for web and mobile that helps users "
        "visualize itineraries, place and annotate locations on interactive maps, manage "
        "trip expenses, and organize trip photography. The product focuses on a high-end, "
        "responsive UX, offline-capable experiences, and performant map interactions."
    ),
    "goals": [
        "Deliver a fast, visually rich itinerary editor and viewer.",
        "Provide an interactive map experience using MapLibre GL JS.",
        "Capture and organize photos tied to places and days.",
        "Track trip expenses with easy entry, categorization, and export.",
        "Support offline-first workflows with background sync.",
    ],
    "features": [
        "Itinerary builder: days, legs, activities, notes, time windows.",
        "Interactive map: pin, cluster, route drawing, heatmaps for photos.",
        "Photo gallery: geotagged photos, albums per trip, lightweight editor.",
        "Expense manager: receipts upload, split costs, currency conversion, export CSV/PDF.",
        "Sharing & collaboration: share trip links, view-only and edit modes.",
        "Offline & background sync: cache maps, optimistic updates, conflict resolution.",
        "Authentication & profiles: OAuth + email, profiles with preferences.",
    ],
    "tech_stack": {
        "frontend": "SvelteKit or Astro (SvelteKit recommended for app-like UX)",
        "styling": "Tailwind CSS with design tokens",
        "map": "MapLibre GL JS (vector tiles)",
        "backend": "Node.js (Fastify/Nest) or serverless functions; PostgreSQL + PostGIS",
        "storage": "S3-compatible for photos",
    },
    "architecture": "Client-first app with server API; media uploads via signed URLs; geospatial data in PostGIS.",
    "data_model": "User, Trip, Day/ItineraryItem, Place, Photo, Expense (see project docs for details)",
    "next_steps": [
        "Finalize product requirements and core user journeys.",
        "Create a lightweight project scaffold for chosen stack.",
        "Implement an interactive prototype: trip creation, place pinning, photo uploads.",
    ],
}

PLAN_TEMPLATE = """# {{ title }}

## Overview
{{ overview }}

## Goals
{% for g in goals %}- {{ g }}
{% endfor %}

## Key Features
{% for f in features %}- {{ f }}
{% endfor %}

## Recommended Tech Stack
- Frontend: {{ tech_stack.frontend }}
- Styling: {{ tech_stack.styling }}
- Map: {{ tech_stack.map }}
- Backend: {{ tech_stack.backend }}
- Storage: {{ tech_stack.storage }}

## Architecture & Data Flow
- {{ architecture }}

## Data Model (high level)
- {{ data_model }}

## Next Steps
{% for step in next_steps %}{{ loop.index }}. {{ step }}
{% endfor %}

_Generated reproducibly by scripts/generate_summaries.py_
"""


class PlanGenerator(BaseGenerator):
    """Generator for ItinerPic project plan."""

    @property
    def output_filename(self) -> str:
        """Output filename for plan document."""
        return "itinerpic_plan.md"

    def get_template(self) -> str:
        """Get plan template."""
        return PLAN_TEMPLATE

    def get_context(self) -> Dict[str, Any]:
        """Get context data for plan template."""
        return PLAN_DATA

    @classmethod
    def from_data(cls, data: Dict[str, Any], **kwargs) -> "PlanGenerator":
        """
        Create generator with custom data.

        Args:
            data: Custom plan data dictionary
            **kwargs: Additional arguments for BaseGenerator

        Returns:
            PlanGenerator instance
        """
        instance = cls(**kwargs)
        # Override context method to use custom data
        instance._custom_data = data
        return instance

    def get_context(self) -> Dict[str, Any]:
        """Get context, preferring custom data if set."""
        if hasattr(self, "_custom_data"):
            return self._custom_data
        return PLAN_DATA

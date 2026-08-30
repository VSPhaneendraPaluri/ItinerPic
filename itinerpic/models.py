from __future__ import annotations

from datetime import datetime, timezone

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Trip(db.Model):
    __tablename__ = "trips"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    destination = db.Column(db.String(200), nullable=False)
    date_range = db.Column(db.String(200), default="Flexible dates")
    budget = db.Column(db.String(80), default="₹0")
    travelers = db.Column(db.String(80), default="2 travelers")
    notes = db.Column(db.Text, default="No extra notes yet.")
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    stops = db.relationship("TripStop", back_populates="trip", cascade="all, delete-orphan")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "destination": self.destination,
            "date_range": self.date_range,
            "budget": self.budget,
            "travelers": self.travelers,
            "notes": self.notes,
            "stops": [stop.to_dict() for stop in self.stops],
            "map_links": _build_map_links([stop.to_dict() for stop in self.stops]),
        }


class TripStop(db.Model):
    __tablename__ = "trip_stops"

    id = db.Column(db.Integer, primary_key=True)
    trip_id = db.Column(db.Integer, db.ForeignKey("trips.id"), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    lat = db.Column(db.String(80), default="")
    lng = db.Column(db.String(80), default="")
    day = db.Column(db.String(80), default="Day 1")
    notes = db.Column(db.Text, default="")
    trip = db.relationship("Trip", back_populates="stops")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "lat": self.lat,
            "lng": self.lng,
            "day": self.day,
            "notes": self.notes,
        }


def _build_map_links(stops: list[dict]) -> dict[str, str]:
    if not stops:
        return {"google": "", "apple": "", "mappls": ""}

    valid_stops = [stop for stop in stops if stop.get("lat") and stop.get("lng")]
    if not valid_stops:
        return {"google": "", "apple": "", "mappls": ""}

    from urllib.parse import urlencode

    origin = f"{valid_stops[0]['lat']},{valid_stops[0]['lng']}"
    destination = f"{valid_stops[-1]['lat']},{valid_stops[-1]['lng']}"
    waypoints = "|".join(f"{stop['lat']},{stop['lng']}" for stop in valid_stops[1:-1])

    google_params = {"api": "1", "origin": origin, "destination": destination}
    if waypoints:
        google_params["waypoints"] = waypoints
    google_maps = "https://www.google.com/maps/dir/?" + urlencode(google_params)

    apple_maps = (
        "https://maps.apple.com/?"
        + urlencode({"t": "m", "dirflg": "d", "daddr": destination})
    )

    mappls_params = {"origin": origin, "destination": destination}
    if waypoints:
        mappls_params["waypoints"] = waypoints
    mappls = "https://www.mappls.com/directions?" + urlencode(mappls_params)

    return {"google": google_maps, "apple": apple_maps, "mappls": mappls}

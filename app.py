from __future__ import annotations

import os
from urllib.parse import urlencode

from flask import Flask, redirect, render_template, request, url_for

from itinerpic.config import Config
from itinerpic.generators.site_generator import get_homepage_data
from itinerpic.models import Trip, TripStop, db


def _trip_to_dict(trip: Trip) -> dict:
    return {
        "id": trip.id,
        "title": trip.title,
        "destination": trip.destination,
        "date_range": trip.date_range,
        "budget": trip.budget,
        "travelers": trip.travelers,
        "notes": trip.notes,
        "stops": [stop.to_dict() for stop in trip.stops],
        "map_links": _build_map_links([stop.to_dict() for stop in trip.stops]),
    }


def _create_trip_from_request(form_data) -> dict | None:
    title = (form_data.get("title") or "My trip").strip()
    destination = (form_data.get("destination") or "Custom destination").strip()
    date_range = (form_data.get("date_range") or "Flexible dates").strip()
    budget = (form_data.get("budget") or "₹0").strip()
    travelers = (form_data.get("travelers") or "2 travelers").strip()
    notes = (form_data.get("notes") or "No extra notes yet.").strip()
    stops = _parse_stops(form_data)

    if not title or not destination:
        return None

    return {
        "title": title,
        "destination": destination,
        "date_range": date_range,
        "budget": budget,
        "travelers": travelers,
        "notes": notes,
        "stops": stops,
        "map_links": _build_map_links(stops),
    }


def _parse_stops(form_data) -> list[dict]:
    names = form_data.getlist("stop_name")
    lats = form_data.getlist("stop_lat")
    lngs = form_data.getlist("stop_lng")
    days = form_data.getlist("stop_day")
    stop_notes = form_data.getlist("stop_notes")

    stops: list[dict] = []
    for index, name in enumerate(names):
        clean_name = (name or "").strip()
        if not clean_name:
            continue

        lat = (lats[index] if index < len(lats) else "").strip()
        lng = (lngs[index] if index < len(lngs) else "").strip()
        day = (days[index] if index < len(days) else "").strip()
        notes = (stop_notes[index] if index < len(stop_notes) else "").strip()

        stops.append(
            {
                "name": clean_name,
                "lat": lat,
                "lng": lng,
                "day": day or "Day 1",
                "notes": notes,
            }
        )

    return stops


def _build_map_links(stops: list[dict]) -> dict[str, str]:
    if not stops:
        return {"google": "", "apple": "", "mappls": ""}

    valid_stops = [stop for stop in stops if stop.get("lat") and stop.get("lng")]
    if not valid_stops:
        return {"google": "", "apple": "", "mappls": ""}

    origin = f"{valid_stops[0]['lat']},{valid_stops[0]['lng']}"
    destination = f"{valid_stops[-1]['lat']},{valid_stops[-1]['lng']}"
    waypoints = "|".join(f"{stop['lat']},{stop['lng']}" for stop in valid_stops[1:-1])

    google_params = {
        "api": "1",
        "origin": origin,
        "destination": destination,
    }
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


def _save_trip_from_request(form_data) -> dict | None:
    trip = _create_trip_from_request(form_data)
    if trip is None:
        return None

    trip_record = Trip(
        title=trip["title"],
        destination=trip["destination"],
        date_range=trip["date_range"],
        budget=trip["budget"],
        travelers=trip["travelers"],
        notes=trip["notes"],
    )
    db.session.add(trip_record)
    db.session.flush()

    for stop in trip["stops"]:
        trip_record.stops.append(
            TripStop(
                name=stop["name"],
                lat=stop["lat"],
                lng=stop["lng"],
                day=stop["day"],
                notes=stop["notes"],
            )
        )

    db.session.commit()
    return _trip_to_dict(trip_record)


def create_app() -> Flask:
    config = Config.get()
    app = Flask(
        __name__,
        template_folder=str(config.templates_dir),
        static_folder=str(config.static_dir),
    )

    database_path = config.project_root / "itinerpic.db"
    database_url = (
        os.getenv("DATABASE_URL")
        or os.getenv("SQLALCHEMY_DATABASE_URI")
        or f"sqlite:///{database_path.as_posix()}"
    )

    app.config.update(
        APP_NAME=config.app_name,
        APP_TITLE=config.app_title,
        SECRET_KEY=config.secret_key,
        DEBUG=config.debug,
        HOST=config.host,
        PORT=config.port,
        SQLALCHEMY_DATABASE_URI=database_url,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )
    db.init_app(app)

    with app.app_context():
        db.create_all()

    @app.route("/", methods=["GET", "POST"])
    def index():
        if request.method == "POST":
            _save_trip_from_request(request.form)
            return redirect(url_for("index"))

        custom_itineraries = [
            _trip_to_dict(trip) for trip in Trip.query.order_by(Trip.id.desc()).all()
        ]
        context = get_homepage_data()
        context["custom_itineraries"] = custom_itineraries

        if custom_itineraries:
            first_trip = custom_itineraries[0]
            context["trip_card"] = {
                "title": first_trip["title"],
                "meta": f"{first_trip['destination']} • {first_trip['date_range']}",
                "snapshot": [
                    {"label": "Days", "value": first_trip["date_range"] or "Flexible"},
                    {"label": "Budget", "value": first_trip["budget"] or "₹0"},
                    {"label": "Travelers", "value": first_trip["travelers"] or "Custom"},
                ],
            }

        return render_template("index.html", **context)

    @app.route("/plan", methods=["GET", "POST"])
    def plan():
        if request.method == "POST":
            _save_trip_from_request(request.form)
            return redirect(url_for("plan"))

        context = get_homepage_data()
        context["custom_itineraries"] = [
            _trip_to_dict(trip) for trip in Trip.query.order_by(Trip.id.desc()).all()
        ]
        return render_template("plan.html", **context)

    return app


app = create_app()


if __name__ == "__main__":
    app.run(
        host=app.config.get("HOST", "0.0.0.0"),
        port=int(app.config.get("PORT", 8000)),
        debug=app.config.get("DEBUG", False),
    )

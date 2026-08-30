from app import create_app


def test_create_app_renders_itinerpic_homepage():
    app = create_app()
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert b"ItinerPic" in response.data
    assert b"Plan the trip" in response.data


def test_custom_trip_is_persisted_in_database():
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    with app.app_context():
        from itinerpic.models import Trip, TripStop, db

        db.session.query(TripStop).delete()
        db.session.query(Trip).delete()
        db.session.commit()
        db.create_all()

    client = app.test_client()
    response = client.post(
        "/",
        data={
            "title": "Paris getaway",
            "destination": "Paris",
            "date_range": "10-15 Sep",
            "budget": "₹30,000",
            "travelers": "2 travelers",
            "notes": "Museum week",
            "stop_name": ["Eiffel Tower", "Louvre"],
            "stop_lat": ["48.8584", "48.8606"],
            "stop_lng": ["2.2945", "2.3376"],
            "stop_day": ["Day 1", "Day 2"],
            "stop_notes": ["Sunset view", "Art day"],
        },
        follow_redirects=True,
    )

    assert response.status_code == 200

    with app.app_context():
        from itinerpic.models import Trip

        trips = Trip.query.all()
        assert len(trips) == 1
        assert trips[0].title == "Paris getaway"
        assert trips[0].destination == "Paris"
        assert len(trips[0].stops) == 2

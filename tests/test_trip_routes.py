from app import create_app


def test_custom_trip_with_stops_generates_route_links():
    app = create_app()
    client = app.test_client()

    response = client.post(
        "/",
        data={
            "title": "Kerala trail",
            "destination": "Kerala",
            "date_range": "2-7 Jan",
            "budget": "₹30,000",
            "travelers": "2 adults",
            "notes": "Family trip",
            "stop_name": ["Munnar", "Alleppey", "Kochi"],
            "stop_lat": ["10.0889", "9.4981", "9.9312"],
            "stop_lng": ["77.0595", "76.3266", "76.2673"],
            "stop_day": ["1", "2", "3"],
            "stop_notes": ["Tea hills", "Backwaters", "Fort area"],
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Kerala trail" in response.data
    assert b"Google Maps" in response.data
    assert b"Mappls" in response.data
    assert b"Apple Maps" in response.data

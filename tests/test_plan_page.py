from app import create_app


def test_landing_page_has_no_create_form_and_plan_page_works():
    app = create_app()
    client = app.test_client()

    home = client.get("/")
    plan = client.get("/plan")

    assert home.status_code == 200
    assert b"Trip name" not in home.data
    assert b"Add itinerary" not in home.data
    assert plan.status_code == 200
    assert b"Trip name" in plan.data

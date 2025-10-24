from app import app

def test_home_route():
    # Use Flask's built-in test client to check home page
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200

def test_about_route():
    client = app.test_client()
    response = client.get('/about')
    assert response.status_code == 200

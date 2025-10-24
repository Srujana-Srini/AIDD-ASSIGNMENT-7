import os
import sys
import pytest

# ✅ Make sure the parent folder (where app.py lives) is on the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app  # Now it can find app.py

def test_home_route():
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200

def test_about_route():
    client = app.test_client()
    response = client.get('/about')
    assert response.status_code == 200
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_stats():
    response = client.get("/stats")
    assert response.status_code == 200
    assert "total_content" in response.json()


def test_process_content():
    payload = {
        "title": "Spring Boot Tutorial",
        "text": "Learn how to build REST APIs with Java and Spring Boot framework."
    }
    response = client.post("/content", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "category" in data
    assert "keywords" in data
    assert "related_content" in data


def test_search():
    payload = {"query": "machine learning python", "top_n": 3}
    response = client.post("/content/search", json=payload)
    assert response.status_code == 200
    assert len(response.json()["results"]) <= 3


def test_categories():
    response = client.get("/content/categories")
    assert response.status_code == 200
    assert "categories" in response.json()


def test_invalid_input():
    # Título muito curto
    payload = {"title": "ab", "text": "texto normal aqui"}
    response = client.post("/content", json=payload)
    assert response.status_code == 422

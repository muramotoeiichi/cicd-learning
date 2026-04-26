import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root():
    """ルートエンドポイントが正しく応答するか"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, CI/CD World!"}


def test_get_item_success():
    """存在するアイテムが正しいJSONで返るか"""
    response = client.get("/items/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "Apple"
    assert data["price"] == 150


def test_get_item_not_found():
    """存在しないアイテムに404が返るか"""
    response = client.get("/items/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"


def test_list_items():
    """アイテム一覧が返るか"""
    response = client.get("/items")
    assert response.status_code == 200
    items = response.json()
    assert len(items) == 3
    # 全アイテムに必要なキーが揃っているか
    for item in items:
        assert "id" in item
        assert "name" in item
        assert "price" in item

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="CI/CD Learning App")

# ダミーデータ（本来はDBに繋ぐところ）
ITEMS = {
    1: {"id": 1, "name": "Apple", "price": 150},
    2: {"id": 2, "name": "Banana", "price": 80},
    3: {"id": 3, "name": "Cherry", "price": 300},
}


class Item(BaseModel):
    id: int
    name: str
    price: int


@app.get("/")
def root():
    return {"message": "Hello, CI/CD World!"}


@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int):
    if item_id not in ITEMS:
        raise HTTPException(status_code=404, detail="Item not found")
    item = ITEMS[item_id]
    # ⚠️ 破壊的変更: キー名を "price" → "cost" に変更（仕様変更のつもりでやりがち）
    return {"id": item["id"], "name": item["name"], "cost": item["price"]}


@app.get("/items", response_model=list[Item])
def list_items():
    return list(ITEMS.values())

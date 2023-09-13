from fastapi import FastAPI

app = FastAPI()

"""
app.get
app.post
app.put
app.delete
"""

# path parameter

@app.get("/")
def read_root():
    return {"Hello": "World"}

# string으로 오는 값을 int로 type casting 시킬 수 있다
@app.get("/items/{item_id}")
def read_rooot(item_id: int):
    item = items[item_id]
    return item


@app.get("/items/{item_id}/{key}")
def read_roooot(item_id: int, key:str):
    item = items[item_id][key]
    return item


# query paratmer

@app.get("/item-by-name")
def read_item_by_name(name: str):
    for item_id, item in items.items():
        if item['name'] == name:
            return item
    return {"error": "data not found"}

# ~/item-by-name?name=bread
# 실행하기 전 위 path parmater 사용한 함수와 구분지어야함


# post

# item 이 어떤 식으로 외부에서 오는지 정의해야 함 pydantic 라이브러리 사용
# get 은 정보를 url 주소에만 담아서 전달
# post는 body 라는 별도 영역있음. 이 영역에 받거나 넘겨주려는 정보를 기입할 수 있음
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: int

@app.post("/items/{item_id}")
def create_item(item_id:int, item: Item):
    if item_id in items:
        return {"error": "there is already existing key"}
    
    items[item_id] = item.dict()
    
    return {"success": "ok"}

from typing import Optional


# Optional은 name. price 모두가 들어오지 않아도 에러 안 뱉게 해줌
class ItemForUpdate(BaseModel):
    name: Optional[str]
    price: Optional[int]


@app.put("/items/{item_id}")
def update_item(item_id:int, item: Item):
    if item_id not in items:
        return {"error": f"there is no item id: {item_id}"}
    
    if item.name:
        items[item_id]['name'] = item.name
    
    if item.price:
        items[item_id]['price'] = item.price

    return {"success": "ok"}


@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    items.pop(item_id)

    return {"success": "ok"}



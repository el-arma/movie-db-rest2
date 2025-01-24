from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from database import SessionLocal, Movie
from sqlalchemy.orm import Session

# Initialize FastAPI app
app = FastAPI()

# Example data storage
items = []


# Define a Pydantic model for an item
class Item(BaseModel):
    id: int
    name: str
    price: float
    in_stock: bool

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def greetings():
    return {"message": "Welcome to my FastAPI demo app!"}

## oginial code
# @app.get("/items/", response_model = List[Item])
# def get_items():
#     return items


# TESTING
@app.get("/movies/")
def get_items(db: Session = Depends(get_db)):
    return db.query(Movie).all()


@app.get("/items/{item_id}", response_model = Item)
def get_item(item_id: int):
    for item in items:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")

# post item
@app.post("/items/", response_model=Item)
def create_item(item: Item):
    items.append(item)
    return item

# update item
@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, updated_item: Item):
    for i, item in enumerate(items):
        if item.id == item_id:
            items[i] = updated_item
            return updated_item
    raise HTTPException(status_code=404, detail="Item not found")

# delete item
@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    global items
    items = [item for item in items if item.id != item_id]
    return {"message": "Item deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host = "127.0.0.1", port = 8000, reload = True)
from fastapi import FastAPI, HTTPException, Depends
from schemas import movie_scheme
from typing import List
from database import SessionLocal, Movie
from sqlalchemy.orm import Session

# Initialize FastAPI app
app = FastAPI()

# Example data storage
items = []


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

# get all movies
@app.get("/movies/")
def get_items(db: Session = Depends(get_db)):
    return db.query(Movie).all()

# get a specific movie
@app.get("/movies/{movie_id}")
def get_item(movie_id: int, db: Session = Depends(get_db)):
    return db.query(Movie).where(Movie.id == movie_id).first()

# post movie or movies
@app.post("/movies/", response_model = List[movie_scheme])
def add_movies(movies: List[movie_scheme], db: Session = Depends(get_db)):
    db_movies = []
    for movie in movies:
        db_movie = Movie(
            imdb_rating=movie.imdb_rating,
            title=movie.title,
            year=movie.year,
            rated=movie.rated,
            runtime=movie.runtime,
            genre=movie.genre,
            director=movie.director,
            actors=movie.actors,
            production=movie.production
        )

        db.add(db_movie)
        db_movies.append(db_movie)
    
    db.commit()

    for db_movie in db_movies:
        db.refresh(db_movie)
    
    return db_movies

# # update item
# @app.put("/items/{item_id}", response_model=Item)
# def update_item(item_id: int, updated_item: Item):
#     for i, item in enumerate(items):
#         if item.id == item_id:
#             items[i] = updated_item
#             return updated_item
#     raise HTTPException(status_code=404, detail="Item not found")

# delete item
@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    global items
    items = [item for item in items if item.id != item_id]
    return {"message": "Item deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host = "127.0.0.1", port = 8000, reload = True)
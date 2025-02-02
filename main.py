from fastapi import FastAPI, HTTPException, Depends
from schemas import movie_scheme
from typing import List
from database import SessionLocal, Movie
from sqlalchemy.orm import Session

# Initialize FastAPI app
app = FastAPI()

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def greetings():
    return {"message": "Welcome to my movie api demo app! 🎞️ "}

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

# update item
@app.put("/movies/{movie_id}", response_model = movie_scheme)
def update_movie(new_data: movie_scheme, movie_id: int, db: Session = Depends(get_db)):
    movie_to_updt = db.query(Movie).where(Movie.id == movie_id).first()
    
    if not movie_to_updt:
        raise HTTPException(status_code=404, detail="Item not found")
    else:
        movie_to_updt.imdb_rating = new_data.imdb_rating
        movie_to_updt.title = new_data.title
        movie_to_updt.year = new_data.year
        movie_to_updt.rated = new_data.rated
        movie_to_updt.runtime = new_data.runtime
        movie_to_updt.genre = new_data.genre
        movie_to_updt.director = new_data.director
        movie_to_updt.actors = new_data.actors
        movie_to_updt.production = new_data.production

        db.add(movie_to_updt)
        db.commit()
        db.refresh(movie_to_updt)
   
    return movie_to_updt

# delete movie
@app.delete("/movies/{movie_id}", response_model = movie_scheme)
def delete_movie(movie_id: int, db: Session = Depends(get_db)):
    movie_to_delete = db.query(Movie).where(Movie.id == movie_id).first()
    
    if not movie_to_delete:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    db.delete(movie_to_delete)
    db.commit()
    
    return movie_to_delete

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host = "127.0.0.1", port = 8000, reload = True)
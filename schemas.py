
from pydantic import BaseModel

# Define a Pydantic model for an movie
class movie_scheme(BaseModel):
    imdb_rating : float
    title: str
    year: int
    rated: str
    runtime: int
    genre: str
    director: str
    actors: str
    production: str
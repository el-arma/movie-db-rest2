from sqlalchemy import Column, Integer, String, Float, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pandas as pd

# SQLAlchemy setup
DATABASE_URL = "sqlite:///./movies.db"
# engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind = engine)

Base = declarative_base()

# Define the Movie table
class Movie(Base):
    __tablename__ = "movies"
    id = Column(Integer, primary_key = True, autoincrement = True)
    imdb_rating = Column(Float, nullable = False)
    title = Column(String, nullable = False)
    year = Column(Integer, nullable = False)
    rated = Column(String, nullable = True)
    runtime = Column(Integer, nullable = True)
    genre = Column(String, nullable = True)
    director = Column(String, nullable = True)
    actors = Column(String, nullable = True)
    production = Column(String, nullable = True)

# Set up SQLite database
def setup_database(db_path = "movies.db"):
    engine = create_engine(f"sqlite:///{db_path}")
    Base.metadata.create_all(engine)
    return engine

# Load CSV and populate database, used only once
def _load_csv_to_db(csv_path, db_engine):
    # Load and clean the CSV
    df = pd.read_csv(csv_path, skipinitialspace=True)

    # Create a session to insert data
    Session = sessionmaker(bind = db_engine)
    session = Session()
    
    # Insert rows into the database
    for _, row in df.iterrows():
        movie = Movie(
            imdb_rating = row["imdb_rating"],
            title = row["title"],
            year = row["year"],
            rated = row.get("rated"),
            runtime = row.get("runtime"),
            genre = row.get("genre"),
            director = row.get("director(s)"),
            actors = row.get("actors"),
            production = row.get("production"),
        )

        session.add(movie)
    
    # Commit and close session
    session.commit()
    session.close()

    print("Data successfully inserted into the database.")


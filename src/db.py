from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


db_url = "postgresql+psycopg2://postgres:password@localhost:5432/main_backend"
engine = create_engine(
    db_url, echo=True
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

connection = engine.connect()

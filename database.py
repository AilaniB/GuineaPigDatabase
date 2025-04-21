from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import Config
from urllib.parse import quote_plus

SQLALCHEMY_DATABASE_URL = (f"mysql+pymysql://{Config.user}:"
                           f"{quote_plus(Config.password)}@{Config.host}:"
                           f"{Config.port}/{Config.database}?charset=utf8mb4")

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


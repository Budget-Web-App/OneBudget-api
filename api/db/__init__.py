from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from api.config import DATABASE_PATH

engine_args = {
    "url": DATABASE_PATH
}

if "sqlite" in DATABASE_PATH:
    engine_args["connect_args"] = {
        "check_same_thread": False
    }

engine = create_engine(**engine_args)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
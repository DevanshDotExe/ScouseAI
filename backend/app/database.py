from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# The user 'Bats1107' was automatically made lowercase 'bats1107' by PostgreSQL.
# We update the username here to match what the database expects.
# Format: "postgresql://user:password@host:port/dbname"
DATABASE_URL = "postgresql://bats1107:Bats1107@localhost:5432/scouseai_feedback"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency to get the DB session in FastAPI endpoints
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

from app.database import engine, Base
from app.models import Feedback

print("Connecting to the database and creating tables...")
try:
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully (if they didn't already exist).")
except Exception as e:
    print(f"An error occurred: {e}")

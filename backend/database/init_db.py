from backend.database.connection import Base, engine
from backend.models.stock import Stock

def init_db():
    # Create the database tables if they don't exist
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
    print("Database database tables created successfully.")

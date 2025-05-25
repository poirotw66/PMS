"""
Database migration script to create/update tables based on our models
"""
import sys
import os

# Add parent directory to path to import from app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import engine
from app import models

def main():
    print("Creating database tables if they don't exist...")
    models.Base.metadata.create_all(bind=engine)
    print("Database migration completed successfully!")

if __name__ == "__main__":
    main()

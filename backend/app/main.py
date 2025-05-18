from fastapi import FastAPI, APIRouter, Depends, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import List
from .models import PotentialCustomer, PotentialCustomerDB, Base # Import Base and PotentialCustomerDB

# Database Configuration (replace with your actual database URL)
# For local testing with PostgreSQL, it might look like:
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@host:port/dbname"
# For Cloud SQL, you'll need to configure connection string, possibly with Cloud SQL Auth Proxy
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:248605@localhost:5432/postgres" # TODO: Replace with actual DB URL

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create database tables if they don't exist
Base.metadata.create_all(bind=engine)

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], # Replace with your frontend origin
    allow_credentials=True,
    allow_methods=["*"] , # Allow all methods
    allow_headers=["*"] , # Allow all headers
)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Potential Customers Router
router = APIRouter(prefix="/potential-customers", tags=["potential-customers"])

@router.post("/", response_model=PotentialCustomer)
def create_potential_customer(customer: PotentialCustomer, db: Session = Depends(get_db)):
    db_customer = PotentialCustomerDB(**customer.model_dump())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

@router.get("/", response_model=List[PotentialCustomer])
@app.get("/potential-customers")
def read_potential_customers(db: Session = Depends(get_db)):
    customers = db.query(PotentialCustomerDB).all()
    return customers

@router.get("/{customer_id}", response_model=PotentialCustomer) # Changed to use ID for lookup
def read_potential_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = db.query(PotentialCustomerDB).filter(PotentialCustomerDB.id == customer_id).first()
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@router.put("/{customer_id}", response_model=PotentialCustomer) # Changed to use ID for lookup
def update_potential_customer(customer_id: int, updated_customer: PotentialCustomer, db: Session = Depends(get_db)):
    db_customer = db.query(PotentialCustomerDB).filter(PotentialCustomerDB.id == customer_id).first()
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")

    for key, value in updated_customer.model_dump().items():
        setattr(db_customer, key, value)

    db.commit()
    db.refresh(db_customer)
    return db_customer

@router.delete("/{customer_id}") # Changed to use ID for lookup
def delete_potential_customer(customer_id: int, db: Session = Depends(get_db)):
    db_customer = db.query(PotentialCustomerDB).filter(PotentialCustomerDB.id == customer_id).first()
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")

    db.delete(db_customer)
    db.commit()
    return {"message": "Customer deleted successfully"}

app.include_router(router)

@app.get("/")
async def read_root():
    return {"message": "Hello World from FastAPI backend!"}

@app.get("/api/v1/health")
async def health_check():
    return {"status": "ok"}
from fastapi import FastAPI, APIRouter, Depends, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import List
from .models import PotentialCustomer, PotentialCustomerDB, Property, PropertyDB, PropertyAsset, PropertyAssetDB, Contract, ContractDB, RepairRequest, RepairRequestDB, Resident, ResidentDB # Import Resident and ResidentDB
from .database import Base # 從 database.py 匯入 Base
from .routers import properties # Import the new properties router

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

# Include the new routers
app.include_router(properties.router)

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

# Property Router
router_properties = APIRouter(prefix="/properties", tags=["properties"])

@router_properties.post("/", response_model=Property)
def create_property(property: Property, db: Session = Depends(get_db)):
    db_property = PropertyDB(**property.model_dump())
    db.add(db_property)
    db.commit()
    db.refresh(db_property)
    return db_property

@router_properties.get("/", response_model=List[Property])
def read_properties(db: Session = Depends(get_db)):
    properties = db.query(PropertyDB).all()
    return properties

@router_properties.get("/{property_id}", response_model=Property)
def read_property(property_id: int, db: Session = Depends(get_db)):
    property = db.query(PropertyDB).filter(PropertyDB.id == property_id).first()
    if property is None:
        raise HTTPException(status_code=404, detail="Property not found")
    return property

@router_properties.put("/{property_id}", response_model=Property)
def update_property(property_id: int, updated_property: Property, db: Session = Depends(get_db)):
    db_property = db.query(PropertyDB).filter(PropertyDB.id == property_id).first()
    if db_property is None:
        raise HTTPException(status_code=404, detail="Property not found")

    for key, value in updated_property.model_dump().items():
        setattr(db_property, key, value)

    db.commit()
    db.refresh(db_property)
    return db_property

@router_properties.delete("/{property_id}")
def delete_property(property_id: int, db: Session = Depends(get_db)):
    db_property = db.query(PropertyDB).filter(PropertyDB.id == property_id).first()
    if db_property is None:
        raise HTTPException(status_code=404, detail="Property not found")

    db.delete(db_property)
    db.commit()
    return {"message": "Property deleted successfully"}

# Property Assets Router
router_property_assets = APIRouter(prefix="/property-assets", tags=["property-assets"])

@router_property_assets.post("/", response_model=PropertyAsset)
def create_property_asset(asset: PropertyAsset, db: Session = Depends(get_db)):
    db_asset = PropertyAssetDB(**asset.model_dump())
    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)
    return db_asset

@router_property_assets.get("/", response_model=List[PropertyAsset])
def read_property_assets(db: Session = Depends(get_db)):
    assets = db.query(PropertyAssetDB).all()
    return assets

@router_property_assets.get("/{asset_id}", response_model=PropertyAsset)
def read_property_asset(asset_id: int, db: Session = Depends(get_db)):
    asset = db.query(PropertyAssetDB).filter(PropertyAssetDB.id == asset_id).first()
    if asset is None:
        raise HTTPException(status_code=404, detail="Property asset not found")
    return asset

@router_property_assets.put("/{asset_id}", response_model=PropertyAsset)
def update_property_asset(asset_id: int, updated_asset: PropertyAsset, db: Session = Depends(get_db)):
    db_asset = db.query(PropertyAssetDB).filter(PropertyAssetDB.id == asset_id).first()
    if db_asset is None:
        raise HTTPException(status_code=404, detail="Property asset not found")

    for key, value in updated_asset.model_dump().items():
        setattr(db_asset, key, value)

    db.commit()
    db.refresh(db_asset)
    return db_asset

@router_property_assets.delete("/{asset_id}")
def delete_property_asset(asset_id: int, db: Session = Depends(get_db)):
    db_asset = db.query(PropertyAssetDB).filter(PropertyAssetDB.id == asset_id).first()
    if db_asset is None:
        raise HTTPException(status_code=404, detail="Property asset not found")

    db.delete(db_asset)
    db.commit()
    return {"message": "Property asset deleted successfully"}

app.include_router(router_property_assets)
app.include_router(router)

@app.get("/")
async def read_root():
    return {"message": "Hello World from FastAPI backend!"}

@app.get("/api/v1/health")
async def health_check():
    return {"status": "ok"}


# Contract Router
router_contracts = APIRouter(prefix="/contracts", tags=["contracts"])

@router_contracts.post("/", response_model=Contract)
def create_contract(contract: Contract, db: Session = Depends(get_db)):
    db_contract = ContractDB(**contract.model_dump())
    db.add(db_contract)
    db.commit()
    db.refresh(db_contract)
    return db_contract

@router_contracts.get("/", response_model=List[Contract])
def read_contracts(db: Session = Depends(get_db)):
    contracts = db.query(ContractDB).all()
    return contracts

@router_contracts.get("/{contract_id}", response_model=Contract)
def read_contract(contract_id: int, db: Session = Depends(get_db)):
    contract = db.query(ContractDB).filter(ContractDB.id == contract_id).first()
    if contract is None:
        raise HTTPException(status_code=404, detail="Contract not found")
    return contract

@router_contracts.put("/{contract_id}", response_model=Contract)
def update_contract(contract_id: int, updated_contract: Contract, db: Session = Depends(get_db)):
    db_contract = db.query(ContractDB).filter(ContractDB.id == contract_id).first()
    if db_contract is None:
        raise HTTPException(status_code=404, detail="Contract not found")

    for key, value in updated_contract.model_dump().items():
        setattr(db_contract, key, value)

    db.commit()
    db.refresh(db_contract)
    return db_contract

@router_contracts.delete("/{contract_id}")
def delete_contract(contract_id: int, db: Session = Depends(get_db)):
    db_contract = db.query(ContractDB).filter(ContractDB.id == contract_id).first()
    if db_contract is None:
        raise HTTPException(status_code=404, detail="Contract not found")

    db.delete(db_contract)
    db.commit()
    return {"message": "Contract deleted successfully"}

app.include_router(router_contracts)

# Repair Requests Router
router_repair_requests = APIRouter(prefix="/repair-requests", tags=["repair-requests"])

@router_repair_requests.post("/", response_model=RepairRequest)
def create_repair_request(request: RepairRequest, db: Session = Depends(get_db)):
    db_request = RepairRequestDB(**request.model_dump())
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return db_request

@router_repair_requests.get("/", response_model=List[RepairRequest])
def read_repair_requests(db: Session = Depends(get_db)):
    requests = db.query(RepairRequestDB).all()
    return requests

@router_repair_requests.get("/{request_id}", response_model=RepairRequest)
def read_repair_request(request_id: int, db: Session = Depends(get_db)):
    request = db.query(RepairRequestDB).filter(RepairRequestDB.id == request_id).first()
    if request is None:
        raise HTTPException(status_code=404, detail="Repair request not found")
    return request

@router_repair_requests.put("/{request_id}", response_model=RepairRequest)
def update_repair_request(request_id: int, updated_request: RepairRequest, db: Session = Depends(get_db)):
    db_request = db.query(RepairRequestDB).filter(RepairRequestDB.id == request_id).first()
    if db_request is None:
        raise HTTPException(status_code=404, detail="Repair request not found")

    for key, value in updated_request.model_dump().items():
        setattr(db_request, key, value)

    db.commit()
    db.refresh(db_request)
    return db_request

@router_repair_requests.delete("/{request_id}")
def delete_repair_request(request_id: int, db: Session = Depends(get_db)):
    db_request = db.query(RepairRequestDB).filter(RepairRequestDB.id == request_id).first()
    if db_request is None:
        raise HTTPException(status_code=404, detail="Repair request not found")

    db.delete(db_request)
    db.commit()
    return {"message": "Repair request deleted successfully"}

app.include_router(router_repair_requests)

# Residents Router
router_residents = APIRouter(prefix="/residents", tags=["residents"])

@router_residents.post("/", response_model=Resident)
def create_resident(resident: Resident, db: Session = Depends(get_db)):
    db_resident = ResidentDB(
        name=resident.name,
        id_number=resident.id_number,
        phone=resident.phone,
        email=resident.email,
        job=resident.job,
        emergency_contact_name=resident.emergency_contact_name,
        emergency_contact_phone=resident.emergency_contact_phone,
        emergency_contact_relationship=resident.emergency_contact_relationship,
        property_id=resident.property_id,
        contract_id=resident.contract_id
    )
    db.add(db_resident)
    db.commit()
    db.refresh(db_resident)
    return db_resident

@router_residents.get("/", response_model=List[Resident])
def read_residents(db: Session = Depends(get_db)):
    residents = db.query(ResidentDB).all()
    return residents

@router_residents.get("/{resident_id}", response_model=Resident)
def read_resident(resident_id: int, db: Session = Depends(get_db)):
    resident = db.query(ResidentDB).filter(ResidentDB.id == resident_id).first()
    if resident is None:
        raise HTTPException(status_code=404, detail="Resident not found")
    return resident

@router_residents.put("/{resident_id}", response_model=Resident)
def update_resident(resident_id: int, resident: Resident, db: Session = Depends(get_db)):
    db_resident = db.query(ResidentDB).filter(ResidentDB.id == resident_id).first()
    if db_resident is None:
        raise HTTPException(status_code=404, detail="Resident not found")
    db_resident.name = resident.name
    db_resident.id_number = resident.id_number
    db_resident.phone = resident.phone
    db_resident.email = resident.email
    db_resident.job = resident.job
    db_resident.emergency_contact_name = resident.emergency_contact_name
    db_resident.emergency_contact_phone = resident.emergency_contact_phone
    db_resident.emergency_contact_relationship = resident.emergency_contact_relationship
    db_resident.property_id = resident.property_id
    db_resident.contract_id = resident.contract_id
    db.commit()
    db.refresh(db_resident)
    return db_resident

@router_residents.delete("/{resident_id}")
def delete_resident(resident_id: int, db: Session = Depends(get_db)):
    db_resident = db.query(ResidentDB).filter(ResidentDB.id == resident_id).first()
    if db_resident is None:
        raise HTTPException(status_code=404, detail="Resident not found")

    db.delete(db_resident)
    db.commit()
    return {"message": "Resident deleted successfully"}

app.include_router(router_residents)
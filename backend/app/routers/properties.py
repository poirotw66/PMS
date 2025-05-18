from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas
from ..database import SessionLocal

router = APIRouter(
    prefix="/properties",
    tags=["properties"]
)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create Property
@router.post("/", response_model=schemas.Property)
def create_property(property: schemas.PropertyCreate, db: Session = Depends(get_db)):
    db_property = models.PropertyDB(**property.model_dump())
    db.add(db_property)
    db.commit()
    db.refresh(db_property)
    return db_property

# Read Properties
from sqlalchemy.orm import joinedload

@router.get("/", response_model=List[schemas.Property])
def read_properties(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    properties = db.query(models.PropertyDB).options(joinedload(models.PropertyDB.assets), joinedload(models.PropertyDB.repair_requests)).offset(skip).limit(limit).all()
    return properties

# Read Single Property
@router.get("/{property_id}", response_model=schemas.Property)
def read_property(property_id: int, db: Session = Depends(get_db)):
    property = db.query(models.PropertyDB).options(joinedload(models.PropertyDB.assets), joinedload(models.PropertyDB.repair_requests)).filter(models.PropertyDB.id == property_id).first()
    if property is None:
        raise HTTPException(status_code=404, detail="Property not found")
    return property

# Update Property
@router.put("/{property_id}", response_model=schemas.Property)
def update_property(property_id: int, property: schemas.PropertyUpdate, db: Session = Depends(get_db)):
    db_property = db.query(models.PropertyDB).filter(models.PropertyDB.id == property_id).first()
    if db_property is None:
        raise HTTPException(status_code=404, detail="Property not found")
    for key, value in property.model_dump(exclude_unset=True).items():
        setattr(db_property, key, value)
    db.commit()
    db.refresh(db_property)
    return db_property

# Delete Property
@router.delete("/{property_id}", response_model=schemas.Property)
def delete_property(property_id: int, db: Session = Depends(get_db)):
    db_property = db.query(models.PropertyDB).filter(models.PropertyDB.id == property_id).first()
    if db_property is None:
        raise HTTPException(status_code=404, detail="Property not found")
    db.delete(db_property)
    db.commit()
    return db_property

# Endpoints for Property Assets
@router.post("/{property_id}/assets/", response_model=schemas.PropertyAsset)
def create_property_asset(property_id: int, asset: schemas.PropertyAssetCreate, db: Session = Depends(get_db)):
    db_property = db.query(models.PropertyDB).filter(models.PropertyDB.id == property_id).first()
    if db_property is None:
        raise HTTPException(status_code=404, detail="Property not found")
    db_asset = models.PropertyAssetDB(**asset.model_dump(), property_id=property_id)
    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)
    return db_asset

@router.get("/{property_id}/assets/", response_model=List[schemas.PropertyAsset])
def read_property_assets(property_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_property = db.query(models.PropertyDB).filter(models.PropertyDB.id == property_id).first()
    if db_property is None:
        raise HTTPException(status_code=404, detail="Property not found")
    assets = db.query(models.PropertyAssetDB).filter(models.PropertyAssetDB.property_id == property_id).offset(skip).limit(limit).all()
    return assets

@router.get("/{property_id}/assets/{asset_id}", response_model=schemas.PropertyAsset)
def read_property_asset(property_id: int, asset_id: int, db: Session = Depends(get_db)):
    db_asset = db.query(models.PropertyAssetDB).filter(models.PropertyAssetDB.property_id == property_id, models.PropertyAssetDB.id == asset_id).first()
    if db_asset is None:
        raise HTTPException(status_code=404, detail="Property asset not found")
    return db_asset

@router.put("/{property_id}/assets/{asset_id}", response_model=schemas.PropertyAsset)
def update_property_asset(property_id: int, asset_id: int, asset: schemas.PropertyAssetUpdate, db: Session = Depends(get_db)):
    db_asset = db.query(models.PropertyAssetDB).filter(models.PropertyAssetDB.property_id == property_id, models.PropertyAssetDB.id == asset_id).first()
    if db_asset is None:
        raise HTTPException(status_code=404, detail="Property asset not found")
    for key, value in asset.model_dump(exclude_unset=True).items():
        setattr(db_asset, key, value)
    db.commit()
    db.refresh(db_asset)
    return db_asset

@router.delete("/{property_id}/assets/{asset_id}", response_model=schemas.PropertyAsset)
def delete_property_asset(property_id: int, asset_id: int, db: Session = Depends(get_db)):
    db_asset = db.query(models.PropertyAssetDB).filter(models.PropertyAssetDB.property_id == property_id, models.PropertyAssetDB.id == asset_id).first()
    if db_asset is None:
        raise HTTPException(status_code=404, detail="Property asset not found")
    db.delete(db_asset)
    db.commit()
    return db_asset

# Endpoints for Repair Requests
@router.post("/{property_id}/repair-requests/", response_model=schemas.RepairRequest)
def create_repair_request(property_id: int, request: schemas.RepairRequestCreate, db: Session = Depends(get_db)):
    db_property = db.query(models.PropertyDB).filter(models.PropertyDB.id == property_id).first()
    if db_property is None:
        raise HTTPException(status_code=404, detail="Property not found")
    db_request = models.RepairRequestDB(**request.model_dump(), property_id=property_id)
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return db_request

@router.get("/{property_id}/repair-requests/", response_model=List[schemas.RepairRequest])
def read_repair_requests(property_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_property = db.query(models.PropertyDB).filter(models.PropertyDB.id == property_id).first()
    if db_property is None:
        raise HTTPException(status_code=404, detail="Property not found")
    requests = db.query(models.RepairRequestDB).filter(models.RepairRequestDB.property_id == property_id).offset(skip).limit(limit).all()
    return requests

@router.get("/{property_id}/repair-requests/{request_id}", response_model=schemas.RepairRequest)
def read_repair_request(property_id: int, request_id: int, db: Session = Depends(get_db)):
    db_request = db.query(models.RepairRequestDB).filter(models.RepairRequestDB.property_id == property_id, models.RepairRequestDB.id == request_id).first()
    if db_request is None:
        raise HTTPException(status_code=404, detail="Repair request not found")
    return db_request

@router.put("/{property_id}/repair-requests/{request_id}", response_model=schemas.RepairRequest)
def update_repair_request(property_id: int, request_id: int, request: schemas.RepairRequestUpdate, db: Session = Depends(get_db)):
    db_request = db.query(models.RepairRequestDB).filter(models.RepairRequestDB.property_id == property_id, models.RepairRequestDB.id == request_id).first()
    if db_request is None:
        raise HTTPException(status_code=404, detail="Repair request not found")
    for key, value in request.model_dump(exclude_unset=True).items():
        setattr(db_request, key, value)
    db.commit()
    db.refresh(db_request)
    return db_request

@router.delete("/{property_id}/repair-requests/{request_id}", response_model=schemas.RepairRequest)
def delete_repair_request(property_id: int, request_id: int, db: Session = Depends(get_db)):
    db_request = db.query(models.RepairRequestDB).filter(models.RepairRequestDB.property_id == property_id, models.RepairRequestDB.id == request_id).first()
    if db_request is None:
        raise HTTPException(status_code=404, detail="Repair request not found")
    db.delete(db_request)
    db.commit()
    return db_request
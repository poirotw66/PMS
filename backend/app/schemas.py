from pydantic import BaseModel
from typing import List, Optional

# Shared properties
class PropertyBase(BaseModel):
    address: str
    size_sq_ft: str
    features: Optional[str] = None

# Properties to receive on creation
class PropertyCreate(PropertyBase):
    pass

# Properties to receive on update
class PropertyUpdate(PropertyBase):
    pass

# Properties to return to client
class Property(PropertyBase):
    id: int
    assets: List["PropertyAsset"] = [] # Forward reference
    repair_requests: List["RepairRequest"] = [] # Forward reference

    class Config:
        from_attributes = True

# Shared properties for Property Asset
class PropertyAssetBase(BaseModel):
    property_id: int
    asset_type: Optional[str] = "家電類"
    purchase_date: Optional[str] = None
    name: str
    purchase_price: Optional[str] = None
    purchase_vendor: Optional[str] = None
    warranty_period: Optional[str] = None
    current_status: Optional[str] = "良好"

# Properties to receive on creation for Property Asset
class PropertyAssetCreate(PropertyAssetBase):
    pass

# Properties to receive on update for Property Asset
class PropertyAssetUpdate(PropertyAssetBase):
    pass

# Properties to return to client for Property Asset
class PropertyAsset(PropertyAssetBase):
    id: int

    class Config:
        from_attributes = True

# Shared properties for Repair Request
class RepairRequestBase(BaseModel):
    tenant_id: int
    property_id: int
    request_date: str
    description: str
    repair_vendor: Optional[str] = None
    repair_cost: Optional[str] = None
    cost_bearer: Optional[str] = None
    resolution_method: Optional[str] = None
    resolution_date: Optional[str] = None
    remarks: Optional[str] = None

# Properties to receive on creation for Repair Request
class RepairRequestCreate(RepairRequestBase):
    pass

# Properties to receive on update for Repair Request
class RepairRequestUpdate(RepairRequestBase):
    pass

# Properties to return to client for Repair Request
class RepairRequest(RepairRequestBase):
    id: int

    class Config:
        from_attributes = True

# Update forward references
Property.model_rebuild()
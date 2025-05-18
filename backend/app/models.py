from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel

Base = declarative_base()

class PotentialCustomerDB(Base):
    __tablename__ = "potential_customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    phone = Column(String)
    needs = Column(String)
    job = Column(String)
    move_in_date = Column(String)  # 新增
    viewing_records = Column(String)  # 新增
    status = Column(String)  # 新增

# Pydantic model for request/response validation
class PotentialCustomer(BaseModel):
    name: str
    phone: str
    needs: str
    job: str
    move_in_date: str | None = None # 新增，允許 None
    viewing_records: str | None = None # 新增，允許 None
    status: str | None = None # 新增，允許 None

    class Config:
        from_attributes = True


class ResidentDB(Base):
    __tablename__ = "residents"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    id_number = Column(String, nullable=True) # 新增：身份證字號
    phone = Column(String)
    email = Column(String, nullable=True)
    job = Column(String, nullable=True) # 新增：工作
    emergency_contact_name = Column(String, nullable=True) # 新增：緊急聯絡人姓名
    emergency_contact_phone = Column(String, nullable=True) # 新增：緊急聯絡人電話
    emergency_contact_relationship = Column(String, nullable=True) # 新增：緊急聯絡人關係
    property_id = Column(String, index=True, nullable=True)
    contract_id = Column(String, index=True, nullable=True)

# Pydantic model for Resident
class Resident(BaseModel):
    id: int | None = None # 新增：允許 ID 為 None，用於新增時
    name: str
    id_number: str | None = None # 新增：身份證字號
    phone: str | None = None
    email: str | None = None
    job: str | None = None # 新增：工作
    emergency_contact_name: str | None = None # 新增：緊急聯絡人姓名
    emergency_contact_phone: str | None = None # 新增：緊急聯絡人電話
    emergency_contact_relationship: str | None = None # 新增：緊急聯絡人關係
    property_id: str | None = None
    contract_id: str | None = None

    class Config:
        from_attributes = True



class PropertyDB(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, index=True) # 物件編號 (內部管理編號)
    address = Column(String, index=True) # 物件地址
    size_sq_ft = Column(String) # 物件坪數 (使用字串以包含單位或備註)
    features = Column(String) # 物件特色

# Pydantic model for Property
class Property(BaseModel):
    address: str
    size_sq_ft: str
    features: str | None = None

    class Config:
        from_attributes = True


# Pydantic model for Resident
class Resident(BaseModel):
    id: int | None = None # 新增：允許 ID 為 None，用於新增時
    name: str
    id_number: str | None = None # 新增：身份證字號
    phone: str | None = None
    email: str | None = None
    job: str | None = None # 新增：工作
    emergency_contact_name: str | None = None # 新增：緊急聯絡人姓名
    emergency_contact_phone: str | None = None # 新增：緊急聯絡人電話
    emergency_contact_relationship: str | None = None # 新增：緊急聯絡人關係
    property_id: str | None = None
    contract_id: str | None = None

    class Config:
        from_attributes = True


class PropertyAssetDB(Base):
    __tablename__ = "property_assets"

    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(Integer, index=True) # 關聯到 PropertyDB 的 ID
    purchase_date = Column(String) # 資產購買日期
    name = Column(String) # 資產名稱/品牌/型號
    purchase_price = Column(String) # 資產購買價格 (使用字串以包含單位或備註)
    purchase_vendor = Column(String) # 購買廠商/電話
    warranty_period = Column(String) # 資產保固期間

# Pydantic model for Property Asset
class PropertyAsset(BaseModel):
    property_id: int
    purchase_date: str | None = None
    name: str
    purchase_price: str | None = None
    purchase_vendor: str | None = None
    warranty_period: str | None = None

    class Config:
        from_attributes = True


# Pydantic model for Resident
class Resident(BaseModel):
    id: int | None = None # 新增：允許 ID 為 None，用於新增時
    name: str
    id_number: str | None = None # 新增：身份證字號
    phone: str | None = None
    email: str | None = None
    job: str | None = None # 新增：工作
    emergency_contact_name: str | None = None # 新增：緊急聯絡人姓名
    emergency_contact_phone: str | None = None # 新增：緊急聯絡人電話
    emergency_contact_relationship: str | None = None # 新增：緊急聯絡人關係
    property_id: str | None = None
    contract_id: str | None = None

    class Config:
        from_attributes = True


class ContractDB(Base):
    __tablename__ = "contracts"

    id = Column(Integer, primary_key=True, index=True) # 合約編號 (內部管理編號)
    property_id = Column(Integer, index=True) # 關聯到 PropertyDB 的 ID
    tenant_id = Column(Integer, index=True) # 關聯到 PotentialCustomerDB 的 ID (承租人)
    start_date = Column(String) # 合約起始日期
    end_date = Column(String) # 合約結束日期
    rent_amount = Column(String) # 租金金額 (使用字串以包含單位或備註)
    payment_frequency = Column(String) # 繳費週期 (例如：月繳、季繳、年繳)
    payment_due_date = Column(String) # 繳費日期 (例如：每月5號)

# Pydantic model for Contract
class Contract(BaseModel):
    property_id: int
    tenant_id: int
    start_date: str
    end_date: str
    rent_amount: str
    payment_frequency: str
    payment_due_date: str

    class Config:
        from_attributes = True


# Pydantic model for Resident
class Resident(BaseModel):
    id: int | None = None # 新增：允許 ID 為 None，用於新增時
    name: str
    id_number: str | None = None # 新增：身份證字號
    phone: str | None = None
    email: str | None = None
    job: str | None = None # 新增：工作
    emergency_contact_name: str | None = None # 新增：緊急聯絡人姓名
    emergency_contact_phone: str | None = None # 新增：緊急聯絡人電話
    emergency_contact_relationship: str | None = None # 新增：緊急聯絡人關係
    property_id: str | None = None
    contract_id: str | None = None

    class Config:
        from_attributes = True


class RepairRequestDB(Base):
    __tablename__ = "repair_requests"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, index=True) # 關聯到 PotentialCustomerDB 的 ID (報修人)
    property_id = Column(Integer, index=True) # 關聯到 PropertyDB 的 ID (報修物件)
    request_date = Column(String) # 報修日期
    description = Column(String) # 報修內容
    resolution_method = Column(String) # 結案方式 (修繕方式及費用)
    resolution_date = Column(String) # 結案日期

# Pydantic model for Repair Request
class RepairRequest(BaseModel):
    tenant_id: int
    property_id: int
    request_date: str
    description: str
    resolution_method: str | None = None
    resolution_date: str | None = None

    class Config:
        from_attributes = True


# Pydantic model for Resident
class Resident(BaseModel):
    id: int | None = None # 新增：允許 ID 為 None，用於新增時
    name: str
    id_number: str | None = None # 新增：身份證字號
    phone: str | None = None
    email: str | None = None
    job: str | None = None # 新增：工作
    emergency_contact_name: str | None = None # 新增：緊急聯絡人姓名
    emergency_contact_phone: str | None = None # 新增：緊急聯絡人電話
    emergency_contact_relationship: str | None = None # 新增：緊急聯絡人關係
    property_id: str | None = None
    contract_id: str | None = None

    class Config:
        from_attributes = True

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
        orm_mode = True

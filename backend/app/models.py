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
    emergency_contact_name = Column(String)
    emergency_contact_phone = Column(String)
    emergency_contact_relationship = Column(String)

# Pydantic model for request/response validation
class PotentialCustomer(BaseModel):
    name: str
    phone: str
    needs: str
    job: str
    emergency_contact_name: str
    emergency_contact_phone: str
    emergency_contact_relationship: str

    class Config:
        orm_mode = True
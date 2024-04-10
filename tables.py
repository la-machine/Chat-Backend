from sqlalchemy import Table, Column, Integer, String, MetaData, Float, Date
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class Supplier(Base):
    __tablename__ = 'supplier'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    contact_name = Column(String)
    email = Column(String)
    phone_number = Column(String)
    address = Column(String)
    products_services_provided = Column(String)
    payment_term = Column(String)
    payment_method = Column(String)
    enterprise_id = Column(Integer)

class Employee(Base):
    __tablename__ = 'employee'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    phone_number = Column(String)
    address = Column(String)
    department = Column(String)
    position = Column(String)
    salary = Column(String)
    hire_date = Column(Date)
    enterprise_id = Column(Integer)


metadata = Base.metadata

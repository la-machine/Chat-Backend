from sqlalchemy import Table, Column, Integer, String, MetaData, Float, Date

# Define the schema for the supplier table
supplier_schema = Table(
    'supplier',
    MetaData(),
    Column('id', Integer, primary_key=True),
    Column('name', String(255), nullable=False),
    Column('email', String(255), nullable=False),
    Column('phone_number', String(50), nullable=False),
    Column('address', String(255), nullable=False),
    Column('product_service_provide', String(255), nullable=False),
    Column('payment_term', String(255), nullable=True),
    Column('payment_methode', Float, nullable=True),
    Column('contact_name', String(255)),
    # Add other columns as needed
)

# Define the schema for the employee table
employee_schema = Table(
    'employee',
    MetaData(),
    Column('id', Integer, primary_key=True),
    Column('name', String(255), nullable=False),
    Column('email', String(255), nullable=False),
    Column('phone_number', String(50), nullable=False),
    Column('address', String(255), nullable=False),
    Column('department', String(255), nullable=False),
    Column('position', String(255), nullable=False),
    Column('salary', Float, nullable=False),
    Column('hire_date', Date),
    # Add other columns as needed
)

from extensions import db

class Enterprise(db.Model):
    __tablename__ = 'enterprises'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    database_name = db.Column(db.String(255), nullable=False)
    database_user = db.Column(db.String(255), nullable=False)
    database_password = db.Column(db.String(255), nullable=False)
    manager_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)
    employees = db.relationship('Employee', backref='enterprise', lazy=True)
    suppliers = db.relationship('Supplier', backref='enterprise', lazy=True)

    def __repr__(self):
        return f'<Enterprise {self.name}>'

    @classmethod
    def get_enterprise_by_name(cls, name):
        return cls.query.filter_by(name = name).first()

    def add_employee(self, employee):
        self.employees.append(employee)
        db.session.commit()

    def add_supplier(self, supplier):
        self.suppliers.append(supplier)
        db.session.commit()

    def set_manager(self, manager_id):
        self.manager_id = manager_id
        db.session.commit()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Employee(db.Model):
    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    department = db.Column(db.String(255), nullable=False)
    position = db.Column(db.String(255), nullable=False)
    salary = db.Column(db.Float, nullable=False)
    hire_date = db.Column(db.String(50), nullable=False)
    termination_date = db.Column(db.String(50))
    enterprise_id = db.Column(db.Integer, db.ForeignKey('enterprises.id'), nullable=True)


    def __repr__(self):
        return f'<Employee {self.name}>'

    @classmethod
    def get_employee_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def get_employee_by_phone_number(cls, phone_number):
        return cls.query.filter_by(phone_number=phone_number).first()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Supplier(db.Model):
    __tablename__ = 'suppliers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    contact_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    products_services_provided = db.Column(db.String(255), nullable=False)
    payment_terms = db.Column(db.String(255), nullable=True)
    payment_method = db.Column(db.String(255), nullable=True)
    enterprise_id = db.Column(db.Integer, db.ForeignKey('enterprises.id'), nullable=True)

    def __repr__(self):
        return f'<Supplier {self.name}>'

    @classmethod
    def get_supplier_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def add_enterprise(self, enterprise):
        self.enterprise.append(enterprise)
        db.session.commit()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

from extensions import db

class Enterprise(db.Model):
    __tablename__ = 'enterprises'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    database_name = db.Column(db.String(255), nullable=False)
    database_user = db.Column(db.String(255), nullable=False)
    database_password = db.Column(db.String(255), nullable=False)
    manager_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)
    employees = db.relationship('User', backref='enterprise', lazy=True, foreign_keys=[manager_id])

    def __repr__(self):
        return f'<Enterprise {self.name}>'

    @classmethod
    def get_enterprise_by_name(cls, name):
        return cls.query.filter_by(name = name).first()

    def add_employee(self, employee):
        self.employees.append(employee)
        db.session.commit()

    def set_manager(self, manager_id):
        self.manager_id = manager_id
        db.session.commit()
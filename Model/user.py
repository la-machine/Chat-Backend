from alembic import op
from extensions import db
from enum import Enum
from .enterprise import Enterprise
from werkzeug.security import generate_password_hash, check_password_hash


class UserRole(Enum):
    ADMIN = 'admin'
    SUPER = 'super_admin'
    USER = 'user'

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=False, nullable=False)
    email = db.Column(db.String(64), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(), nullable=False)
    role = db.Column(db.Enum(UserRole), default=UserRole.USER, nullable=False)
    enterprise_id = db.Column(db.Integer, db.ForeignKey('enterprises.id'), nullable=True)


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

        # Getter method for enterprise
        @property
        def get_enterprise(self):
            return self._enterprise

        # Setter method for enterprise
        @enterprise.setter
        def set_enterprise(self, value):
            if not isinstance(value, Enterprise):
                raise ValueError("Enterprise must be an instance of Enterprise class")
            self._enterprise = value

    def __repr__(self):
        return f'<User {self.email}>'

    @classmethod
    def get_user_by_email(cls,email):
        return cls.query.filter_by(email = email).first()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

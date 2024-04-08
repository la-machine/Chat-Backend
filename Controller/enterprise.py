from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt
from Model.user import User, UserRole
# from extensions import db
from sqlalchemy_utils import database_exists, create_database
from Model.enterprise import Enterprise
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
import tables


ent_bp = Blueprint('ent', __name__)
# def initialize_tables(database_name):
#     with db.engine.connect() as connection:
#         connection.execute(f"USE {database_name}")
#         tables.supplier_schema.create(bind=db.engine, checkfirst=True)
#         tables.employee_schema.create(bind=db.engine, checkfirst=True)

@ent_bp.post('/register')
@jwt_required()
def register_enterprise():
    claims = get_jwt()

    if claims.get('role') != 'super_admin':
        return jsonify({"Message": "You are not authorize to access this"}), 401
    data = request.get_json()
    enterprise = Enterprise.get_enterprise_by_name(name=data.get('name'))
    if enterprise is not None:
        return jsonify({"error": "Enterprise already exists!"})

    new_enterprise = Enterprise(
        name = data.get('name'),
        database_name = data.get('db_name'),
        database_user = data.get('db_user'),
        database_password = data.get('db_password')
    )

    try:

        engine = create_engine(f"postgresql+psycopg2://{data.get('db_user')}:{data.get('db_password')}@localhost:5432/{data.get('db_name')}")
        if not database_exists(engine.url):
            create_database(engine.url)
        tables.supplier_schema.create(bind=engine, checkfirst=True)
        tables.employee_schema.create(bind=engine, checkfirst=True)

        new_enterprise.save()

    except OperationalError as e:
        return jsonify({"error": f"Failed to create or initialize database: {str(e)}"}), 500

    user = User.get_user_by_email(email = data.get('email'))
    if user is None:
        return jsonify({"error":"No user with this email Please make sure this user enail is created"})

        # user = new_user
    user.set_enterprise(new_enterprise.id)
    user.save()
    new_enterprise.set_manager(manager_id=user.id)

    new_enterprise.save()
    # user.save()

    return jsonify({"Message": "Enterprise created!"}) , 201

# def addEmployee (employee):
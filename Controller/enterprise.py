from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt
from Model.user import User, UserRole
from extensions import db
from Model.enterprise import Enterprise
from sqlalchemy.exc import OperationalError
import tables


ent_bp = Blueprint('ent', __name__)
def initialize_tables(database_name):
    with db.engine.connect() as connection:
        connection.execute(f"USE {database_name}")
        tables.supplier_schema.create(bind=db.engine, checkfirst=True)
        tables.employee_schema.create(bind=db.engine, checkfirst=True)

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


    # try:
    #
    #     # Create the database if it does not exist
    #     with db.engine.connect() as connection:
    #         connection.execute(f"CREATE DATABASE IF NOT EXISTS {data.get('db_name')}")
    #
    #     # Initialize the tables for the new enterprise
    #     initialize_tables(data.get('db_name'))
    #
    #     # Save the enterprise to get its ID
    #     new_enterprise.save()
    #
    # except OperationalError as e:
    #     return jsonify({"error": f"Failed to create or initialize database: {str(e)}"}), 500

    user = User.get_user_by_email(email = data.get('email'))
    if user is None:
        new_user = User(
            username=data.get('username'),
            email=data.get('email'),
            role=UserRole.ADMIN
        )
        user = new_user
        user.set_password(password=data.get('password'))
        user.set_enterprise(new_enterprise.id)
        user.save()
        # user = new_user
    new_enterprise.set_manager(manager_id=user.id)

    new_enterprise.save()
    # user.save()

    return jsonify({"Message": "Enterprise created!"}) , 201

# def addEmployee (employee):
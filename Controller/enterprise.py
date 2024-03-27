from flask import Blueprint, jsonify, request
from Model.user import User, db, UserRole
from Model.enterprise import Enterprise


auth_bp = Blueprint('auth', __name__)
@auth_bp.post('/register')
def register_enterprise():
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

    user = User.get_user_by_email(email = data.get('email'))
    if user is not None:
        new_user = User(
            username=data.get('username'),
            email=data.get('email'),
            enterprise=enterprise,
            role=UserRole.ADMIN
        )

        new_user.set_password(password=data.get('password'))


    new_user.save()

    return jsonify({"Message": "User created!"})

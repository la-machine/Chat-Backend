from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, create_refresh_token,jwt_required, get_jwt
from Model.user import User, db, UserRole
from Model.enterprise import Enterprise, Employee


auth_bp = Blueprint('auth', __name__)
@auth_bp.post('/register')
def register_user():
    data = request.get_json()
    user = User.get_user_by_email(email = data.get('email'))
    if user is not None:
        return jsonify({"error": "User already exists!"}) , 403
    # enterprise = Enterprise.get_enterprise_by_name(name = data.get('enterprise'))
    new_user = User(
        username = data.get('username'),
        email = data.get('email'),
        role = UserRole.SUPER
    )
    new_user.set_password(password = data.get('password'))
    new_user.save()

    return jsonify({"Message": "User created!"}) , 201

@auth_bp.post('/register/manager')
def register_manager():
    data = request.get_json()
    user = User.get_user_by_email(email = data.get('email'))
    if user is not None:
        return jsonify({"error": "User already exists!"}) , 403

    # enterprise = Enterprise.get_enterprise_by_name(name = data.get('enterprise'))
    # if enterprise is None:
    #     return jsonify({"error":"No enterprise with this name"}) , 403

    new_user = User(
        username = data.get('username'),
        email = data.get('email'),
        role = UserRole.ADMIN
    )
    new_user.set_password(password = data.get('password'))
    new_user.save()

    return jsonify({"Message": "User created!"}) , 201

@auth_bp.post('/register/employee')
def register_employee():
    claims = get_jwt()

    if claims.get('role') != 'admin' or claims.get('role') != 'super_admin':
        return jsonify({"Message":"You are not authorize to access this"}) , 401

    data = request.get_json()
    user = Employee.get_user_by_email(email = data.get('email'))

    if user is not None:
        return jsonify({"error": "User already exists!"}) , 403

    enterprise = Enterprise.get_enterprise_by_name(name = data.get('enterprise'))

    if enterprise is None:
        return jsonify({"error":"No enterprise with this name"}) , 403

    employee = Employee(name=data.get('Name'),
                        email=data.get('Email'),
                        phone_number=data.get('Phone'),
                        address=data.get('Address'),
                        department=data.get('Department'),
                        position=data.get('Position'),
                        salary=data.get('Salary'),
                        hire_date=data.get('Hire_date'),
                        # termination_date='',
                        enterprise_id=1)
    # termination_date=data.get('Termination Date'))
    Employee.save(employee)

    return jsonify({"Message": "Employee Added!"}) , 201

@auth_bp.post('/login')
def user_login():
    data = request.get_json()

    user = User.get_user_by_email(email = data.get('email'))

    if user and (user.check_password(password = data.get('password'))):
        access_token = create_access_token(identity=user.email)
        refresh_token = create_refresh_token(identity = user.email)
        return jsonify({
            "message":"Logged In",
            "token" : {
                "access":access_token,
                "refresh":refresh_token
            },
            "role": user.role.value,
            "name": user.username,
            "email": user.email
        }) , 200
    return jsonify({"error":"invalid credentials"}), 400

@auth_bp.get('/whoami')
@jwt_required()

def whoami():
    claims = get_jwt()
    return jsonify({"message":"message", "claims":claims})
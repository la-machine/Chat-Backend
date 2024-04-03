from flask import Flask, jsonify
from extensions import db, jwt
from Controller.authentication import auth_bp
from Controller.users import user_bp
from Controller.enterprise import ent_bp
from Model.user import User
from flask_cors import CORS

from dotenv import load_dotenv

from test import chat_bp

load_dotenv()


def create_app():

    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})

    app.config.from_prefixed_env()
    # app.config.from_envvar('APP_SETTINGS')

    #Initialize the databse
    db.init_app(app)
    jwt.init_app(app)
    with app.app_context():
        db.create_all()
    # Register blueprints
    app.register_blueprint(auth_bp,url_prefix = '/api/auth')
    app.register_blueprint(user_bp, url_prefix = '/api/user')
    app.register_blueprint(ent_bp, url_prefix = '/api/enterprise')
    app.register_blueprint(chat_bp, url_prefix = '/api')

    @jwt.additional_claims_loader
    def add_extra_claims(identity):
        user = User.get_user_by_email(email=identity)
        if user is not None:
            return {"role" : user.role.value}

    @jwt.expired_token_loader
    def expired_token_collback(jwt_header, jwt_data):
        return jsonify({"message":"Token has expire", "error":"token expired"}), 401

    @jwt.invalid_token_loader
    def invalid_token_collback(error):
        return  jsonify({"message":"Signature verification failed", "error":"Invalid Token"}), 401

    @jwt.unauthorized_loader
    def missing_token_collback(error):
        return jsonify({"message":"Request does not contain a valid token", "error":"authorization_header"}), 401


    return app

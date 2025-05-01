from flask import Flask, redirect, url_for, render_template, jsonify, request, session
from .config import Config
from .extension import db, jwt, login_manager
from .utils.to_sql import json_to_sql
from .models.model import UserAccount
from .models.forms import LoginForm
from .extension import message_handler, reader
from flask_login import current_user

app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)
jwt.init_app(app)
login_manager.init_app(app)

def create_app():

    from .routes.auth import auth_bp
    from .routes.viewes import view_bp
    from .routes.py_js import admin_bp


    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(view_bp, url_prefix='/api')
    app.register_blueprint(admin_bp)

    with app.app_context():
        db.create_all()
        json_to_sql()

    @login_manager.user_loader
    def load_user(user_id):
        return UserAccount.query.get(int(user_id))
    
    @jwt.expired_token_loader
    def expired_token(jwt_header, jwt_payload):
        return jsonify(
            "Token has expired you have to get a new token"), 401
    
    @jwt.invalid_token_loader
    def invalid_token(error):
        return jsonify(
            "Invalid Token "), 401
    
    @jwt.unauthorized_loader
    def missing_token(error):

        return render_template('index.html', name=current_user.username), 401
    
    @jwt.revoked_token_loader
    def revoked_token(jwt_header, jwt_payload):
        #Blacllsted tokens
        return jsonify(
            "Bloced Token: get a new by login token>"), 401

    @app.errorhandler(404)
    def page_not_found(e):
        return redirect(url_for('auth_bp.logIn'))
        
    return app
    
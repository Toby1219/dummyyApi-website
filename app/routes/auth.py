from flask import Blueprint, render_template, redirect, flash, url_for, jsonify
from ..models.model import UserAccount
from ..schemas.schema import UserAccSchema
from ..extension import db
from ..config import Config
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required
from datetime import datetime
from ..extension import message_handler
from flask_login import login_user, logout_user, current_user 
from ..models.forms import LoginForm, RegisterForm

auth_bp = Blueprint("auth_bp", __name__)

def gen_token(username, role):
    token = create_access_token(identity=username, 
                                    additional_claims={'role':role},
                                    expires_delta=Config.JWT_ACCESS_TOKEN_EXPIRES)        
    refresh_token_ = create_refresh_token(identity=username, 
                                             additional_claims={'role':role},
                                             expires_delta=Config.JWT_REFRESH_TOKEN)
    issued = datetime.now()
    exp = issued + Config.JWT_ACCESS_TOKEN_EXPIRES
    return token, refresh_token_, issued, exp

@auth_bp.route("/signin", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        account_name = UserAccount.query.filter_by(username=form.username.data).first()
        account_email = UserAccount.query.filter_by(email=form.email.data).first()
        if account_name:
            flash("User name already exist", "error")
        elif account_email:
            flash("Email already exist", 'error')
        else:
            tk, r_tk, issued, exp = gen_token(username=form.username.data, role='user')
            user = UserAccount(username=form.username.data, email=form.email.data, role="user",
                               token=tk, refresh_token=r_tk, 
                               token_created_at=str(issued), token_exp_at=str(exp))
            user.set_password(form.password.data)
            user.create_user()
            login_user(user)
            flash('Registered successfully!')
            return redirect(url_for('view_bp.home'))
    return render_template('register.html', form=form), 200


@auth_bp.route("/login", methods=['GET', 'POST'])
def logIn():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = UserAccount.query.filter_by(username=username).first()
        print(user)
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('view_bp.home'))
        else:
            flash("Invalid log in details", "error")
    return render_template("login.html", form=form)


@auth_bp.route('/refresh', methods=["GET"])
@jwt_required(refresh=True)
def refresh():
    if not current_user.is_authenticated:
        return jsonify({"Message":"login to refresh token"}), 404
    t, r_t, issu, exp = gen_token(current_user.username, "user")
    user = UserAccount.query.get(current_user.id)
    if not user:
        return jsonify({"mesage":"user invalid"})
    user.token = t
    user.refresh_token =r_t
    user.token_created_at = issu
    user.token_exp_at = exp
    db.session.commit()
    return jsonify({"token":t, "refresh_token":r_t}), 200

@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth_bp.logIn'))

@auth_bp.route("/whoami")
def whoami():
    if not current_user.is_authenticated:
        return redirect(url_for('auth_bp.logIn'))
    user = UserAccount.query.get(current_user.id)
    schema = UserAccSchema(exclude=["id", "password_hash", "role"])
    data = schema.dump(user)
    message_handler(f"viewing profile of {current_user.username}")
    return jsonify(data)




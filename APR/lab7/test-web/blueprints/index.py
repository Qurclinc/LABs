import hashlib

from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user, login_required, login_user, logout_user

from extensions import db
from models import User

router = Blueprint("index", __name__, template_folder="templates")

@router.route("/", methods=["GET", "POST"])
def index():
    if current_user.is_authenticated:
        return redirect(url_for("index.me"))
    return redirect(url_for("index.login"))

@router.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = request.form
        login = data.get("login")
        password = data.get("password")
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        user: User | None = db.session.execute(
            db.Select(User)
            .where(User.login == login)
        ).scalar_one_or_none()
        
        if not(user):
            flash(f"Не существует пользователя с логином {login}", "fail")
            return render_template("login.html")
        
        if user.password != hashed_password:
            flash(f"Неверный логин или пароль", "fail")
            return render_template("login.html")
        
        login_user(user)
        
        return redirect(url_for("index.me"))
        
    return render_template("login.html")

@router.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index.login"))

@router.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        data = request.form
        login = data.get("login")
        
        existing = db.session.execute(
            db.Select(User).where(User.login == login)
        ).scalar_one_or_none()

        if existing:
            flash("Пользователь уже существует", "fail")
            return render_template("register.html")
        
        password = data.get("password")
        password2 = data.get("confirm")
        if password != password2:
            flash("Пароли не совпадают", "fail")
            return render_template("register.html")
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        user = User(login=login, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        
        flash("Аккаунт успешно зарегистрирован", "success")
        
    return render_template("register.html")

@router.route("/me")
@login_required
def me():
    return render_template("profile.html")
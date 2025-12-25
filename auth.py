from flask import Blueprint, render_template, request, redirect, session,jsonify
from extensions import db
import bcrypt
from werkzeug.security import generate_password_hash

auth_bp = Blueprint("auth", __name__)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"<User {self.email}>"

    def generate_password_hash(self, password):
        self.password = generate_password_hash(password)

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        if User.query.filter_by(email=email).first():
            return render_template("register.html", error="Email already exists")

        user = User(email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect("/login")

    return render_template("register.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            session["user_id"] = user.id
            return redirect("/dashboard")

        return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

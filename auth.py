from flask import Blueprint, render_template, request, redirect, session,jsonify,make_response,current_app
from extensions import db
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime, timedelta
import jwt
from functools import wraps

auth_bp = Blueprint("auth", __name__)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"<User {self.email}>"

    def generate_password_hash(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        if User.query.filter_by(email=email).first():
            return render_template("register.html", error="Email already exists")
        
        user = User(name=name, email=email)
        user.generate_password_hash(password)
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

        if not user or not user.check_password(password):
            return render_template("login.html", error="Invalid credentials")

        # 🔐 Create JWT
        token = jwt.encode(
            {
                "user_id": user.id,
                "exp": datetime.utcnow() + timedelta(hours=1)
            },
            current_app.config["SECRET_KEY"],
            algorithm="HS256"
        )

        # 🍪 Store JWT in HTTP-only cookie
        response = make_response(redirect(f"/dashboard/{user.name}"))
        response.set_cookie(
            "access_token",
            token,
            httponly=True,
            samesite="Lax",
            secure=False
        )

        return response

    return render_template("login.html")

@auth_bp.route("/logout")
def logout():
    response = make_response(redirect("/login"))
    response.delete_cookie("access_token")
    return response

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get("access_token")

        if not token:
            return redirect("/login")

        try:
            data = jwt.decode(
                token,
                current_app.config["SECRET_KEY"],
                algorithms=["HS256"]
            )
            current_user = User.query.get(data["user_id"])
        except jwt.ExpiredSignatureError:
            return redirect("/login")
        except jwt.InvalidTokenError:
            return redirect("/login")

        return f(current_user, *args, **kwargs)

    return decorated
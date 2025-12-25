from flask import Blueprint, render_template, request, redirect,make_response
from extensions import db
from auth import User, token_required
from datetime import datetime

dashboard_bp = Blueprint("dashboard", __name__)

# =====================
# Expense Model
# =====================
class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


# =====================
# Dashboard Route
# =====================
@dashboard_bp.route("/dashboard/<name>")
@token_required
def dashboard(current_user, name):
    """
    current_user comes from token_required (JWT)
    name comes from the URL (/dashboard/<name>)
    """

    # 🔐 Security check: URL name must match logged-in user
    if current_user.name != name:
        return redirect(f"/dashboard/{current_user.name}")

    expenses = Expense.query.filter_by(
        user_id=current_user.id
    ).all()

    return render_template(
        "dashboard.html",
        user=current_user,
        expenses=expenses
    )


# =====================
# Add Expense Route
# =====================
@dashboard_bp.route("/add_expense", methods=["GET", "POST"])
@token_required
def add_expense(current_user):

    if request.method == "POST":
        expense = Expense(
            amount=float(request.form["amount"]),
            description=request.form["description"],
            user_id=current_user.id
        )

        db.session.add(expense)
        db.session.commit()

        return redirect(f"/dashboard/{current_user.name}")

    return render_template("add_expense.html")


@dashboard_bp.route("/logout", methods=["GET", "POST"])
def logout():
    response = make_response(redirect("/login"))
    response.delete_cookie("access_token")
    return response

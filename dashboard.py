from flask import Blueprint, render_template, request, redirect, session
from app import db
from auth import User
from datetime import datetime

dashboard_bp = Blueprint("dashboard", __name__)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@dashboard_bp.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/login")

    expenses = Expense.query.filter_by(
        user_id=session["user_id"]
    ).all()

    return render_template("dashboard.html", expenses=expenses)

@dashboard_bp.route("/add_expense", methods=["GET", "POST"])
def add_expense():
    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":
        expense = Expense(
            amount=float(request.form["amount"]),
            description=request.form["description"],
            user_id=session["user_id"]
        )
        db.session.add(expense)
        db.session.commit()
        return redirect("/dashboard")

    return render_template("add_expense.html")

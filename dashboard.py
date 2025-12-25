from flask import Blueprint, render_template, request, redirect,make_response
from extensions import db
from auth import User, token_required
from datetime import datetime

dashboard_bp = Blueprint("dashboard", __name__)


class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


@dashboard_bp.route("/dashboard/<name>")
@token_required
def dashboard(current_user, name):
    
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

    return render_template("add_expense.html", user=current_user)


@dashboard_bp.route("/delete_expense/<int:expense_id>", methods=["POST"])
@token_required
def delete_expense(current_user, expense_id):
    expense = Expense.query.get_or_404(expense_id)

    if expense.user_id != current_user.id:
        return redirect(f"/dashboard/{current_user.name}")

    db.session.delete(expense)
    db.session.commit()

    return redirect(f"/dashboard/{current_user.name}")

@dashboard_bp.route("/edit_expense/<int:expense_id>", methods=["GET", "POST"])
@token_required
def edit_expense(current_user, expense_id):
    expense = Expense.query.get_or_404(expense_id)

    if expense.user_id != current_user.id:
        return redirect(f"/dashboard/{current_user.name}")

    if request.method == "POST":
        expense.amount = float(request.form["amount"])
        expense.description = request.form["description"]

        db.session.commit()

        return redirect(f"/dashboard/{current_user.name}")

    return render_template("edit_expense.html", user=current_user, expense=expense)

@dashboard_bp.route("/logout", methods=["GET", "POST"])
def logout():
    response = make_response(redirect("/login"))
    response.delete_cookie("access_token")
    return response

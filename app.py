from flask import Flask,redirect,request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'
db = SQLAlchemy(app)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<Expense {self.description}: {self.amount}>'

@app.route("/register" , methods=['GET','POST'])
def register():
    if request.method == 'POST':
        # Handle registration logic here
        return redirect("/login")
    return "Hello world!"

@app.route("/login" , methods=['GET','POST'])
def login():
    if request.method == 'POST':
        # Handle login logic here
        return redirect("/dashboard")
    return "Hello world!"

if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'super_secret_key'

db = SQLAlchemy(app)

# IMPORT BLUEPRINTS AFTER app & db
from auth import auth_bp
from dashboard import dashboard_bp

# REGISTER BLUEPRINTS
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)

@app.route("/")
def home():
    return redirect("/login")

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)

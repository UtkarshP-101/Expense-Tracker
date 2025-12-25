from flask import Flask, redirect
from extensions import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'super_secret_key'

db.init_app(app)

# Import Blueprints
from auth import auth_bp
from dashboard import dashboard_bp

app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)

@app.route("/")
def home():
    return redirect("/login")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

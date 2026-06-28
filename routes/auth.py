from flask import Blueprint, request, jsonify, session, render_template, redirect
from werkzeug.security import check_password_hash
from database.models import User

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    # Jika pengunjung mengakses via browser biasa, tampilkan halaman login
    if request.method == "GET":
        # Jika sudah login, jangan biarkan di halaman login, lempar ke dashboard
        if session.get("logged_in"):
            return redirect("/")
        return render_template("login.html")

    # Jika pengunjung menekan tombol submit (POST)
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    # Cari user di database Supabase
    user = User.query.filter_by(username=username).first()

    # Validasi dan Enkripsi
    if user and check_password_hash(user.password_hash, password):
        session["logged_in"] = True
        session["username"] = user.username
        return jsonify({"status": "success", "message": "Akses Diberikan."}), 200
    else:
        return jsonify({"status": "error", "message": "Kredensial tidak valid!"}), 401

@auth_bp.route("/logout")
def logout():
    session.clear() # Hancurkan tiket masuk
    return redirect("/auth/login")
from app import app
from database.db import db
from database.models import User
from werkzeug.security import generate_password_hash

def inject_admin():
    with app.app_context():
        print("Mencoba terhubung ke Supabase...")
        
        # 1. Tentukan Kredensial (Ganti password ini nanti jika ingin lebih aman)
        target_username = "admin"
        target_password = "password123" 
        
        # 2. Cek apakah admin sudah pernah dibuat sebelumnya
        existing_user = User.query.filter_by(username=target_username).first()
        
        if existing_user:
            print(f"⚠️ Eksekusi Dibatalkan: Akun dengan username '{target_username}' sudah ada di database.")
            return

        # 3. Enkripsi Password (Hashing)
        print("Mengenkripsi kata sandi...")
        hashed_pw = generate_password_hash(target_password)
        
        # 4. Suntikkan ke Database
        new_admin = User(username=target_username, password_hash=hashed_pw)
        db.session.add(new_admin)
        db.session.commit()
        
        print("="*50)
        print("✅ INJEKSI BERHASIL!")
        print(f"Username : {target_username}")
        print(f"Password : {target_password}")
        print("="*50)
        print("Silakan gunakan kredensial di atas untuk login ke Dashboard.")

if __name__ == "__main__":
    inject_admin()
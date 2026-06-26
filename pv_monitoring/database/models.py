from datetime import datetime
from database.db import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    username = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


class PVData(db.Model):
    __tablename__ = "pv_data"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    timestamp = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    lux = db.Column(
        db.Float,
        nullable=False
    )

    temperature = db.Column(
        db.Float,
        nullable=False
    )

    voltage = db.Column(
        db.Float,
        nullable=False
    )

    current = db.Column(
        db.Float,
        nullable=False
    )

    power = db.Column(
        db.Float,
        nullable=False
    )

    condition = db.Column(
        db.String(20),
        nullable=False
    )
    
    # Kolom untuk menyimpan nilai Confidence dari AI
    confidence = db.Column(
        db.Float, 
        nullable=True, 
        default=0.0
    )
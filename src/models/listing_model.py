from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import random

# Initialize DB here (Single Source of Truth)
db = SQLAlchemy()

class Listing(db.Model):
    __tablename__ = 'listings'

    id = db.Column(db.Integer, primary_key=True)
    
    # --- NEW: Link to the User who owns this ---
    provider_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    
    # --- NEW: The Verification Badge ---
    is_verified = db.Column(db.Boolean, default=False) 
    
    # Standard Fields
    title = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.String(50), nullable=False)
    contact = db.Column(db.String(20), nullable=False)
    
    # Location
    address = db.Column(db.String(200), nullable=False)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    
    # Ratings
    rating = db.Column(db.Float, default=0.0)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "category": self.category,
            "is_verified": self.is_verified,  # Send this to frontend/bot
            "location": {
                "address": self.address,
                "lat": self.latitude,
                "lon": self.longitude
            },
            "price": self.price,
            "rating": f"{self.rating}★",
            "contact": self.contact
        }
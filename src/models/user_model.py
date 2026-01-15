from src.models.listing_model import db  # Import the SAME db instance
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(50), nullable=True)
    
    # Roles: 'client', 'provider', 'admin'
    role = db.Column(db.String(20), default='client') 
    
    # Trust Score
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship: One User can have MANY Listings
    listings = db.relationship('Listing', backref='provider', lazy=True)

    def __repr__(self):
        return f"<User {self.name} ({self.role})>"
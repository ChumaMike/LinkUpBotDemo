from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Listing(db.Model):
    __tablename__ = 'listings'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False, index=True)
    description = db.Column(db.Text, nullable=True) # New: Details about the job/service
    
    # Location Data (The "Plan C" Feature)
    address = db.Column(db.String(200), nullable=False) # e.g. "480 Mofokeng St, Soweto"
    latitude = db.Column(db.Float, nullable=True)  # e.g. -26.2345
    longitude = db.Column(db.Float, nullable=True) # e.g. 27.9876
    
    # Trust Metrics (The "Plan A" Feature)
    price = db.Column(db.String(50), nullable=False)
    contact = db.Column(db.String(20), nullable=False)
    rating = db.Column(db.Float, default=0.0) # 0 to 5 stars
    review_count = db.Column(db.Integer, default=0)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "category": self.category,
            "location": {
                "address": self.address,
                "lat": self.latitude,
                "lon": self.longitude
            },
            "price": self.price,
            "rating": f"{self.rating}★ ({self.review_count} reviews)",
            "contact": self.contact
        }
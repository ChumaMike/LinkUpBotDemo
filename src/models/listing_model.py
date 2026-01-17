from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Listing(db.Model):
    __tablename__ = 'listings'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False) # service, house, job
    price = db.Column(db.String(50))
    contact = db.Column(db.String(50))
    # Ensure this column matches exactly what we use in the service
    address = db.Column(db.String(200)) 
    
    # Provider linking
    provider_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    is_verified = db.Column(db.Boolean, default=False)
    rating = db.Column(db.Float, default=0.0)
    
    # Location data
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        """
        Converts the database object to a simple dictionary 
        so the Bot can read it easily.
        """
        return {
            'id': self.id,
            'title': self.title,
            'category': self.category,
            'price': self.price,
            'contact': self.contact,
            'address': self.address,  # <--- THIS WAS LIKELY MISSING!
            'is_verified': self.is_verified,
            'rating': self.rating,
            'latitude': self.latitude,
            'longitude': self.longitude
        }
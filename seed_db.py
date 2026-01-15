from src import create_app
from src.models.listing_model import db, Listing
from src.models.user_model import User

app = create_app()

with app.app_context():
    print("🗑️  Cleaning old database...")
    db.drop_all()
    db.create_all()
    
    # 1. Create Users (Providers)
    print("👤 Creating Users...")
    
    # A Verified Provider (e.g., You verified his ID)
    user_joe = User(phone_number="27123456789", name="Joe The Plumber", role="provider")
    
    # An Unverified Public User (e.g., Random person posting)
    user_random = User(phone_number="27999888777", name="Random Guy", role="client")
    
    db.session.add(user_joe)
    db.session.add(user_random)
    db.session.commit() # Commit to get IDs
    
    # 2. Create Listings linked to Users
    print("🏠 Creating Listings...")
    
    listings = [
        Listing(
            title="Joe's Premium Plumbing", 
            category="service", 
            price="R350/hr", 
            contact=user_joe.phone_number,
            address="Maponya Mall, Soweto", 
            latitude=-26.2514, longitude=27.8967, 
            rating=4.8,
            provider_id=user_joe.id,  # Linked to Joe
            is_verified=True          # ✅ VERIFIED
        ),
        Listing(
            title="Cheap Backyard Room", 
            category="house", 
            price="R1000", 
            contact="071112233",
            address="Orlando East", 
            latitude=-26.2360, longitude=27.9100, 
            rating=0.0,
            provider_id=user_random.id, # Linked to Random Guy
            is_verified=False           # ⚠️ NOT VERIFIED
        )
    ]
    
    db.session.add_all(listings)
    db.session.commit()
    print("✅ Database successfully seeded with Users and Verified Listings!")
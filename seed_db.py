from src import create_app
from src.models.listing_model import db, Listing

app = create_app()

# Dummy Data with Real Coordinates (Soweto/JHB areas)
dummy_data = [
    {
        "title": "Joe's Plumbing", "category": "service", "price": "R300/hr", "contact": "0123456789",
        "address": "Maponya Mall, Soweto", "lat": -26.2514, "lon": 27.8967, "rating": 4.5
    },
    {
        "title": "Mama's Cleaning", "category": "service", "price": "R200/visit", "contact": "0987654321",
        "address": "Orlando West, Soweto", "lat": -26.2365, "lon": 27.9142, "rating": 5.0
    },
    {
        "title": "Braamfontein Loft", "category": "house", "price": "R5000", "contact": "011223344",
        "address": "Braamfontein, JHB", "lat": -26.1929, "lon": 28.0305, "rating": 4.0
    }
]

with app.app_context():
    db.drop_all()
    db.create_all()
    
    for item in dummy_data:
        listing = Listing(
            title=item["title"],
            category=item["category"],
            price=item["price"],
            contact=item["contact"],
            address=item["address"],
            latitude=item["lat"],
            longitude=item["lon"],
            rating=item["rating"]
        )
        db.session.add(listing)
    
    db.session.commit()
    print("✅ Database seeded with Geo-Location data!")
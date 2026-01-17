from run import app
from src.models.user_model import db, User

# REPLACE THIS WITH YOUR PHONE NUMBER (The one you use to login)
MY_PHONE = "+27123456789" 

with app.app_context():
    # Find your user
    me = User.query.filter_by(phone_number=MY_PHONE).first()
    
    if me:
        me.role = "admin"
        db.session.commit()
        print(f"👑 SUCCESS: {me.name} is now an ADMIN!")
    else:
        print("❌ User not found. Check the phone number.")
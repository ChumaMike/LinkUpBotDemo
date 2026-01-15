from flask import Blueprint, render_template
from flask_login import login_required, current_user
from src.models.listing_model import Listing

web_bp = Blueprint('web', __name__)

@web_bp.route("/")
def home():
    """The Landing Page"""
    return render_template("home.html")

@web_bp.route("/map")
def map_view():
    """The Map Dashboard"""
    listings = Listing.query.all()
    data = [item.to_dict() for item in listings]
    # We now render a NEW template called 'map_pro.html' (see Phase 3)
    return render_template("map_pro.html", listings=data)


@web_bp.route("/dashboard")
@login_required  # <--- SECURITY: Rejects anyone who isn't logged in
def dashboard():
    # 1. If they are a Provider, show THEIR listings only
    if current_user.role == 'provider':
        my_listings = Listing.query.filter_by(provider_id=current_user.id).all()
        return render_template("dashboard.html", user=current_user, listings=my_listings)
    
    # 2. If they are an Admin (You), show EVERYTHING
    elif current_user.role == 'admin':
        all_listings = Listing.query.all()
        return render_template("dashboard.html", user=current_user, listings=all_listings)
    
    # 3. Regular clients just see the profile
    return render_template("dashboard.html", user=current_user, listings=[])
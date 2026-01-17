from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from src.models.listing_model import db, Listing
from geopy.geocoders import Nominatim
# --- NEW: Import the AI Brain ---
from src.services.ai_service import ai_brain 

web_bp = Blueprint('web', __name__)

@web_bp.route("/")
def home():
    """The Landing Page"""
    return render_template("home.html")

@web_bp.route("/map")
def map_view():
    """The Map Dashboard (Public View)"""
    listings = Listing.query.all()
    data = [item.to_dict() for item in listings]
    return render_template("map_pro.html", listings=data)

@web_bp.route("/dashboard")
@login_required
def dashboard():
    # 1. Get the raw database objects for this provider
    raw_listings = Listing.query.filter_by(provider_id=current_user.id).all()
    
    # 2. Convert to Dictionaries (Fixes "Not JSON Serializable" error)
    listings_data = [item.to_dict() for item in raw_listings]
    
    # 3. Send Clean Data to template
    return render_template("dashboard.html", user=current_user, listings=listings_data)

@web_bp.route("/listings/add", methods=["POST"])
@login_required
def add_listing():
    title = request.form.get("title")
    category = request.form.get("category")
    price = request.form.get("price")
    address = request.form.get("address")

    existing_listing = Listing.query.filter_by(
        title=title, 
        provider_id=current_user.id
    ).first()

    if existing_listing:
        flash("You have already posted this service! Edit the existing one instead.", "warning")
        return redirect(url_for("web.dashboard"))
    
    # --- 1. GEOCODING (Get Real Location) ---
    lat, lon = None, None
    try:        
        geolocator = Nominatim(user_agent="linkup_geo_app")
        # Append country to ensure local results
        location = geolocator.geocode(f"{address}, South Africa")
        
        if location:
            lat = location.latitude
            lon = location.longitude
        else:
            # Fallback: Soweto Center
            lat = -26.2514
            lon = 27.8967
            
    except Exception as e:
        print(f"Geocoding Error: {e}")
        lat = -26.2514
        lon = 27.8967

    # --- 2. AI AUTO-TAGGING (The New Brain) ---
    # We ask Gemini to generate search keywords based on the title
    try:
        generated_tags = ai_brain.generate_keywords(title, category)
        print(f"🏷️ Auto-generated tags: {generated_tags}")
    except Exception as e:
        print(f"⚠️ Tagging Failed: {e}")
        generated_tags = title.lower() # Fallback

    # --- 3. SAVE TO DB ---
    new_listing = Listing(
        title=title,
        category=category,
        price=price,
        contact=current_user.phone_number,
        address=address,
        provider_id=current_user.id,
        is_verified=True,
        rating=5.0,
        latitude=lat,
        longitude=lon,
        keywords=generated_tags  # <--- Saving the AI tags here
    )
    
    db.session.add(new_listing)
    db.session.commit()
    
    flash("Listing created on the map with AI Tags!", "success")
    return redirect(url_for("web.dashboard"))

@web_bp.route("/listings/edit/<int:listing_id>", methods=["GET", "POST"])
@login_required
def edit_listing(listing_id):
    # 1. Find the listing
    listing = Listing.query.get_or_404(listing_id)
    
    # 2. Security Check
    if listing.provider_id != current_user.id and current_user.role != 'admin':
        flash("You are not authorized to edit this listing.", "error")
        return redirect(url_for("web.dashboard"))

    # 3. Handle the Save (POST)
    if request.method == "POST":
        listing.title = request.form.get("title")
        listing.category = request.form.get("category")
        listing.price = request.form.get("price")
        listing.address = request.form.get("address")
        
        # Optional: You could re-run AI tagging here if the title changed
        # listing.keywords = ai_brain.generate_keywords(listing.title, listing.category)
        
        db.session.commit()
        flash("Listing updated successfully!", "success")
        return redirect(url_for("web.dashboard"))

    # 4. Handle the View (GET)
    return render_template("edit_listing.html", listing=listing)
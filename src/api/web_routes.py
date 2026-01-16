from flask import Blueprint, render_template
from flask_login import login_required, current_user
from src.models.listing_model import db, Listing
from flask import request, redirect, url_for, flash

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

@web_bp.route("/listings/add", methods=["POST"])
@login_required
def add_listing():
    # 1. Get data from form
    title = request.form.get("title")
    category = request.form.get("category")
    price = request.form.get("price")
    address = request.form.get("address")
    
    # 2. Validation (Basic)
    if not title or not price:
        flash("Title and Price are required!", "error")
        return redirect(url_for("web.dashboard"))

    # 3. Create Listing
    # NOTE: For now, we are hardcoding a location near Soweto for all new pins 
    # so they show up on the map. Later we can add a "Pin Picker".
    import random
    base_lat = -26.2514
    base_lon = 27.8967
    
    new_listing = Listing(
        title=title,
        category=category,
        price=price,
        contact=current_user.phone_number, # Use the user's phone
        address=address,
        provider_id=current_user.id,
        is_verified=True, # Auto-verify logic for now
        rating=5.0,
        # Randomize location slightly so pins don't stack perfectly on top of each other
        latitude=base_lat + (random.uniform(-0.01, 0.01)),
        longitude=base_lon + (random.uniform(-0.01, 0.01))
    )
    
    db.session.add(new_listing)
    db.session.commit()
    
    flash("Listing created successfully!", "success")
    return redirect(url_for("web.dashboard"))

@web_bp.route("/listings/edit/<int:listing_id>", methods=["GET", "POST"])
@login_required
def edit_listing(listing_id):
    # 1. Find the listing
    listing = Listing.query.get_or_404(listing_id)
    
    # 2. Security Check: Ensure the logged-in user OWNS this listing
    # (Admins can edit anything)
    if listing.provider_id != current_user.id and current_user.role != 'admin':
        flash("You are not authorized to edit this listing.", "error")
        return redirect(url_for("web.dashboard"))

    # 3. Handle the Save (POST)
    if request.method == "POST":
        listing.title = request.form.get("title")
        listing.category = request.form.get("category")
        listing.price = request.form.get("price")
        listing.address = request.form.get("address")
        
        db.session.commit() # Save changes
        flash("Listing updated successfully!", "success")
        return redirect(url_for("web.dashboard"))

    # 4. Handle the View (GET) - Show the form
    return render_template("edit_listing.html", listing=listing)
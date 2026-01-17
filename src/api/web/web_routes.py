from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
# We need to import ALL the models here to avoid "NameError"
from src.models.listing_model import Listing, JobRequest, Lead

web_bp = Blueprint('web', __name__)

@web_bp.route("/")
def home():
    """The Landing Page"""
    return render_template("web/home.html")

@web_bp.route("/map")
def map_view():
    """The Public Map"""
    listings = Listing.query.filter_by(is_verified=True).all()
    data = [item.to_dict() for item in listings]
    return render_template("web/map_pro.html", listings=data)

@web_bp.route("/dashboard")
@login_required
def dashboard():
    # ---------------------------------------------------------
    # SCENARIO 1: PROVIDER LOGIN (Business Owner)
    # ---------------------------------------------------------
    if current_user.role == 'provider':
        # 1. Fetch My Listings
        raw_listings = Listing.query.filter_by(provider_id=current_user.id).all()
        listings_data = [item.to_dict() for item in raw_listings]
        
        # 2. Fetch My Leads (Incoming customers)
        # We assume Lead model exists now. If not, this list is empty.
        try:
            my_leads = Lead.query.filter_by(provider_id=current_user.id).order_by(Lead.created_at.desc()).all()
        except:
            my_leads = [] # Fallback if table doesn't exist yet
        
        # 3. Render Provider Dashboard
        # NOTICE: We use key=value for everything. No lists allowed as arguments.
        return render_template("web/dashboard.html", 
                               user=current_user, 
                               listings=listings_data, 
                               leads=my_leads)

    # ---------------------------------------------------------
    # SCENARIO 2: CUSTOMER LOGIN (Client)
    # ---------------------------------------------------------
    elif current_user.role == 'customer':
        # 1. Fetch My Active Job Requests
        try:
            my_jobs = JobRequest.query.filter_by(customer_id=current_user.id).order_by(JobRequest.created_at.desc()).all()
        except:
            my_jobs = []

        # 2. Fetch All Verified Listings (For the Map)
        all_listings = Listing.query.filter_by(is_verified=True).all()
        map_data = [item.to_dict() for item in all_listings]
        
        # 3. Render Customer Dashboard
        return render_template("web/customer_dashboard.html", 
                               user=current_user, 
                               jobs=my_jobs,       
                               listings=map_data)   

    # ---------------------------------------------------------
    # SCENARIO 3: ADMIN LOGIN
    # ---------------------------------------------------------
    elif current_user.role == 'admin':
        return redirect(url_for('admin.admin_panel'))
    
    # Fallback
    return redirect(url_for('web.home'))
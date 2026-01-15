from flask import Blueprint, render_template
from src.models.listing_model import Listing

web_bp = Blueprint('web', __name__)

@web_bp.route("/")
@web_bp.route("/map")
def map_view():
    # 1. Fetch ALL listings from the DB
    listings = Listing.query.all()
    
    # 2. Convert to a list of dicts for the Javascript to use
    data = [item.to_dict() for item in listings]
    
    # 3. Render the HTML page
    return render_template("map.html", listings=data)
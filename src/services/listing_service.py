from src.models.listing_model import Listing, db
from src.utils.geo_utils import calculate_distance

class ListingService:
    
    def get_listings_near_me(self, category, user_lat, user_lon, radius_km=10):
        """
        Finds listings within a specific radius of the user.
        """
        # 1. Get all listings in that category
        all_listings = Listing.query.filter_by(category=category.lower()).all()
        
        nearby_results = []
        
        # 2. Filter by distance
        for item in all_listings:
            dist = calculate_distance(user_lat, user_lon, item.latitude, item.longitude)
            
            if dist <= radius_km:
                # Add distance to the object so we can show "2.5km away"
                item_data = item.to_dict()
                item_data['distance_km'] = round(dist, 1)
                nearby_results.append(item_data)
        
        # 3. Sort by nearest first (or by rating!)
        nearby_results.sort(key=lambda x: x['distance_km'])
        
        return nearby_results

def format_listings_response(self, listings, city_or_context):
        if not listings:
            return f"No listings found nearby."
        
        reply = f"*Found {len(listings)} results near {city_or_context}:*\n\n"
        
        for item in listings:
            # 1. Check the Verification Status
            badge = "✅ *VERIFIED*" if item.get('is_verified') else "⚠️ _Unverified_"
            
            # 2. Format the Message
            rating_str = item.get('rating', 'New')
            dist = item.get('distance_km', '?')
            
            reply += (f"📍 *{item['title']}* {badge}\n"
                      f"   Distance: {dist}km away\n"
                      f"   💰 {item['price']} | ⭐ {rating_str}\n"
                      f"   📞 {item['contact']}\n\n")
        return reply
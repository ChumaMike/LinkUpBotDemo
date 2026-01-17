from src.models.listing_model import Listing
from src.utils.geo_utils import calculate_distance

class ListingService:
    
    def get_listings_near_me(self, category, user_lat, user_lon, radius_km=50):
        """
        Finds listings within X km of the user's GPS coordinates.
        """
        all_listings = Listing.query.all()
        nearby_listings = []

        for item in all_listings:
            # Filter by Category (if specific)
            if category and category != 'service' and item.category != category:
                continue

            # Calculate Distance
            dist = calculate_distance(user_lat, user_lon, item.latitude, item.longitude)
            
            if dist <= radius_km:
                item_data = item.to_dict()
                item_data['distance'] = round(dist, 1)
                nearby_listings.append(item_data)

        # Sort by distance (closest first)
        nearby_listings.sort(key=lambda x: x['distance'])
        return nearby_listings

    def get_listings(self, location, category, keyword=None):
        """
        [UPGRADED] Searches by Location, Category, AND Specific Keywords (Title).
        """
        try:
            query = Listing.query
            
            # 1. Filter by Category
            if category and category != 'service':
                query = query.filter(Listing.category == category)
                
            # 2. Filter by Location
            if location and isinstance(location, str) and location.lower() != 'near me':
                query = query.filter(Listing.address.contains(location))

            # 3. [NEW] Filter by Keyword (e.g., "Car Wash", "Plumber")
            if keyword:
                # We look for the keyword in the Title OR the Category
                # using 'ilike' for case-insensitive search (works in SQLite as simple filter usually)
                search_term = f"%{keyword}%"
                query = query.filter(Listing.title.ilike(search_term))
            
            results = query.all()
            return [item.to_dict() for item in results]

        except Exception as e:
            print(f"⚠️ Search Error: {e}")
            return []

    def format_listings_response(self, listings, context):
        """
        Turns the list of data into a nice WhatsApp message.
        """
        if not listings:
            return f"🚫 Sorry, I couldn't find any listings for *{context}*.\n\nTry sending your 📍 Location Pin to find people nearby."
        
        message = f"🔍 *Found {len(listings)} results for {context}:*\n\n"
        
        for item in listings[:5]:  # Limit to top 5
            dist_info = f" (📍 {item['distance']}km away)" if 'distance' in item else ""
            verified_badge = "✅" if item['is_verified'] else "⚠️"
            
            message += (
                f"*{item['title']}* {verified_badge}\n"
                f"💰 {item['price']}\n"
                f"📞 {item['contact']}\n"
                f"🏠 {item['address']}{dist_info}\n"
                f"------------------\n"
            )
            
        message += "\nReply with *'Menu'* to start over."
        return message
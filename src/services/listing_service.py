import json
import os

class ListingService:
    def __init__(self, data_file="listings.json"):
        self.data_file = data_file
        self.listings = self._load_data()

    def _load_data(self):
        # Enterprise Safety: Handle missing files gracefully
        if not os.path.exists(self.data_file):
            print(f"Error: {self.data_file} not found.")
            return []
        try:
            with open(self.data_file, "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            print(f"Error: {self.data_file} contains invalid JSON.")
            return []

    def get_listings(self, city, category):
        """
        Filters listings by city and category.
        """
        results = [
            item for item in self.listings
            if item["category"] == category and item["city"] == city
        ]
        return results

    def format_listings_response(self, listings, city, category):
        """
        Formats the list of objects into a WhatsApp-friendly string.
        """
        if not listings:
            return f"No {category}s found in {city}."
        
        reply = f"*{category.capitalize()} listings in {city.capitalize()}:*\n"
        for item in listings:
            reply += f"• {item['title']} - {item['price']}\n  Call: {item['contact']}\n"
        
        return reply
import json

with open("listings.json", "r") as file:
    listings = json.load(file)


prices = listings["rosebank"]["houses"]

print(f"city is: \n" + "\n".join(prices))
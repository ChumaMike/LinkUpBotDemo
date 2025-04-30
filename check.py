import json

with open("listings.json", "r") as file:
    listings = json.load(file)


prices = listings["Rosebank"]["houses"]

print(f"city is: \n" + "\n".join(prices))
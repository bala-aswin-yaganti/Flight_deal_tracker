from dotenv import load_dotenv
load_dotenv()

import os
from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager

data_manager = DataManager()
flight_search = FlightSearch()
notifier = NotificationManager()

# Step 1: Update IATA codes
data_manager.update_iata_codes()

# Step 2: Get flight data
deals = data_manager.get_destinations()

# Step 3: Search and notify
for deal in deals:
    from_code = deal["iataFrom"]
    to_code = deal["iataTo"]
    target_price = deal["lowestPrice"]

    flight = flight_search.search_flight(from_code, to_code)

    if flight and flight["price"] < target_price:
        msg = (
            f"Low price alert! Only ₹{flight['price']} to fly from "
            f"{flight['cityFrom']} to {flight['cityTo']} on {flight['dateFrom']}."
        )

        notifier.send_sms(msg)
        notifier.send_email("Flight Deal Alert", msg, os.getenv("EMAIL"))

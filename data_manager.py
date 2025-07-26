import json
import os
import requests
from dotenv import load_dotenv

load_dotenv()

SHEETY_ENDPOINT = os.getenv("SHEETY_ENDPOINT")

class DataManager:
    def __init__(self, iata_file="data/iata_codes.json"):
        with open(iata_file, "r") as file:
            self.iata_codes = json.load(file)

    def get_sheet_data(self):
        response = requests.get(SHEETY_ENDPOINT)
        response.raise_for_status()
        return response.json()["sheet1"]

    def update_iata_codes(self):
        data = self.get_sheet_data()
        for row in data:
            from_city = row["cityFrom"]
            to_city = row["cityTo"]
            updated_data = {}

            if from_city in self.iata_codes:
                updated_data["iataFrom"] = self.iata_codes[from_city]

            if to_city in self.iata_codes:
                updated_data["iataTo"] = self.iata_codes[to_city]

            if updated_data:
                body = {"sheet1": updated_data}
                response = requests.put(f"{SHEETY_ENDPOINT}/{row['id']}", json=body)
                response.raise_for_status()

    def get_destinations(self):
        return self.get_sheet_data()

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import phonenumbers
from phonenumbers import geocoder, carrier
from opencage.geocoder import OpenCageGeocode
import folium
import uuid
import os

# ✅ Create folder before mounting
os.makedirs("maps", exist_ok=True)

# 🚀 Init app
app = FastAPI()

# Allow frontend to access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:5173"] for stricter access
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🗺️ Mount /maps folder
app.mount("/maps", StaticFiles(directory="maps"), name="maps")

# 🔐 OpenCage API Key
key = "08900e1704fd4204b0718910e8174931"
geocode = OpenCageGeocode(key)

# 📦 Request model
class PhoneNumberRequest(BaseModel):
    number: str

# 📍 POST endpoint
@app.post("/track")
def track_number(data: PhoneNumberRequest):
    try:
        number = data.number.strip()
        parsed = phonenumbers.parse(number)

        location = geocoder.description_for_number(parsed, "en")
        service = carrier.name_for_number(parsed, "en")

        result = geocode.geocode(location)
        if not result:
            return {"error": "Location not found"}

        lat = result[0]['geometry']['lat']
        lng = result[0]['geometry']['lng']

        filename = f"{uuid.uuid4()}.html"
        filepath = os.path.join("maps", filename)

        map_obj = folium.Map(location=[lat, lng], zoom_start=9)
        folium.Marker([lat, lng], popup=location).add_to(map_obj)
        map_obj.save(filepath)

        return {
            "location": location,
            "carrier": service,
            "latitude": lat,
            "longitude": lng,
            "map_url": f"http://localhost:8080/maps/{filename}"
        }

    except Exception as e:
        return {"error": f"Tracking failed: {str(e)}"}

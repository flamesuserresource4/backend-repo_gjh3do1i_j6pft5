import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from bson import ObjectId

from database import db, create_document, get_documents
from schemas import Service, Stylist, Testimonial, Booking, Contact

app = FastAPI(title="Salon API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Salon API running"}

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        if db is not None:
            response["database"] = "✅ Connected & Working"
            response["database_url"] = "✅ Set"
            response["database_name"] = getattr(db, 'name', None) or "Unknown"
            response["connection_status"] = "Connected"
            try:
                response["collections"] = db.list_collection_names()
            except Exception as e:
                response["collections"] = [f"Error listing: {str(e)[:60]}"]
        else:
            response["database"] = "❌ Not Connected"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:80]}"
    return response

# Seed minimal content if empty (idempotent)
@app.post("/seed")
def seed_content():
    try:
        # If no services, add a few
        if db["service"].count_documents({}) == 0:
            services = [
                Service(title="Signature Haircut", description="Precision cut + wash + style", price=799, duration_minutes=45, category="Hair", image="/images/haircut.jpg").model_dump(),
                Service(title="Global Hair Color", description="Ammonia-free color for all hair", price=2499, duration_minutes=120, category="Hair", image="/images/color.jpg").model_dump(),
                Service(title="Detan Facial", description="Glow facial for instant brightening", price=1199, duration_minutes=60, category="Skin", image="/images/facial.jpg").model_dump(),
            ]
            db["service"].insert_many(services)
        # If no stylists, add a few
        if db["stylist"].count_documents({}) == 0:
            stylists = [
                Stylist(name="Ayesha Khan", specialty="Color & Balayage", experience_years=7, rating=4.9, bio="Known for dimensional color.", avatar="/images/ayesha.jpg").model_dump(),
                Stylist(name="Rohit Sharma", specialty="Men's Grooming", experience_years=9, rating=4.8, bio="Skin fades and beard styling expert.", avatar="/images/rohit.jpg").model_dump(),
                Stylist(name="Meera Patel", specialty="Bridal & Makeup", experience_years=6, rating=4.9, bio="Subtle glam bridal looks.", avatar="/images/meera.jpg").model_dump(),
            ]
            db["stylist"].insert_many(stylists)
        # Testimonials
        if db["testimonial"].count_documents({}) == 0:
            testimonials = [
                Testimonial(name="Shruti", message="Best balayage in town!", rating=5).model_dump(),
                Testimonial(name="Arjun", message="Super relaxing facial.", rating=4.5).model_dump(),
                Testimonial(name="Nisha", message="Loved the haircut and vibe!", rating=5).model_dump(),
            ]
            db["testimonial"].insert_many(testimonials)
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Public endpoints
@app.get("/services")
def list_services():
    docs = get_documents("service")
    for d in docs:
        d["_id"] = str(d.get("_id"))
    return docs

@app.get("/stylists")
def list_stylists():
    docs = get_documents("stylist")
    for d in docs:
        d["_id"] = str(d.get("_id"))
    return docs

@app.get("/testimonials")
def list_testimonials():
    docs = get_documents("testimonial")
    for d in docs:
        d["_id"] = str(d.get("_id"))
    return docs

# Booking and contact
@app.post("/book")
def create_booking(payload: Booking):
    booking_id = create_document("booking", payload)
    return {"id": booking_id, "message": "Booking request received"}

@app.post("/contact")
def send_contact(payload: Contact):
    contact_id = create_document("contact", payload)
    return {"id": contact_id, "message": "Message received"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

"""
Database Schemas for Salon App

Each Pydantic model represents a MongoDB collection. The collection name is the
lowercase of the class name (e.g., Service -> "service").
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class Service(BaseModel):
    title: str = Field(..., description="Service title, e.g., Haircut, Coloring")
    description: Optional[str] = Field(None, description="Short description of the service")
    price: float = Field(..., ge=0, description="Base price in INR")
    duration_minutes: int = Field(..., ge=10, le=480, description="Estimated duration in minutes")
    category: Optional[str] = Field(None, description="Category like Hair, Skin, Nails")
    image: Optional[str] = Field(None, description="Preview image URL")

class Stylist(BaseModel):
    name: str = Field(..., description="Stylist full name")
    specialty: str = Field(..., description="Primary specialty, e.g., Color, Bridal, Men")
    experience_years: int = Field(..., ge=0, le=60, description="Years of experience")
    rating: float = Field(4.8, ge=0, le=5, description="Average rating")
    bio: Optional[str] = Field(None, description="Short bio")
    avatar: Optional[str] = Field(None, description="Avatar image URL")

class Testimonial(BaseModel):
    name: str = Field(..., description="Customer name")
    message: str = Field(..., description="Feedback message")
    rating: float = Field(..., ge=0, le=5, description="Star rating")
    date: datetime = Field(default_factory=datetime.utcnow, description="Review date")

class Booking(BaseModel):
    service_id: str = Field(..., description="Selected service _id as string")
    stylist_id: Optional[str] = Field(None, description="Selected stylist _id as string")
    name: str = Field(..., description="Customer full name")
    phone: str = Field(..., description="WhatsApp/phone number")
    date: str = Field(..., description="YYYY-MM-DD")
    time: str = Field(..., description="HH:MM 24h format")
    notes: Optional[str] = Field(None, description="Extra notes")

class Contact(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    message: str

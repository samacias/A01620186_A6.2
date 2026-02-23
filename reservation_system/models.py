"""Data models for hotels, customers, and reservations."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class Hotel:
    """Hotel entity."""
    hotel_id: str
    name: str
    rooms: int
    location: str

    def to_dict(self) -> dict[str, Any]:
        """Convert hotel to dictionary for JSON storage."""
        return {
            "hotel_id": self.hotel_id,
            "name": self.name,
            "rooms": self.rooms,
            "location": self.location,
        }

    @staticmethod
    def from_dict(data: dict[str, Any]) -> "Hotel":
        """Create a Hotel object from a dictionary."""
        return Hotel(
            hotel_id=str(data["hotel_id"]),
            name=str(data["name"]),
            rooms=int(data["rooms"]),
            location=str(data["location"]),
        )


@dataclass
class Customer:
    """Customer entity."""
    customer_id: str
    name: str
    email: str

    def to_dict(self) -> dict[str, Any]:
        """Convert customer to dictionary for JSON storage."""
        return {
            "customer_id": self.customer_id,
            "name": self.name,
            "email": self.email,
        }

    @staticmethod
    def from_dict(data: dict[str, Any]) -> "Customer":
        """Create a Customer object from a dictionary."""
        return Customer(
            customer_id=str(data["customer_id"]),
            name=str(data["name"]),
            email=str(data["email"]),
        )


@dataclass
class Reservation:
    """Reservation entity."""
    reservation_id: str
    hotel_id: str
    customer_id: str
    room: int

    def to_dict(self) -> dict[str, Any]:
        """Convert reservation to dictionary for JSON storage."""
        return {
            "reservation_id": self.reservation_id,
            "hotel_id": self.hotel_id,
            "customer_id": self.customer_id,
            "room": self.room,
        }

    @staticmethod
    def from_dict(data: dict[str, Any]) -> "Reservation":
        """Create a Reservation object from a dictionary."""
        return Reservation(
            reservation_id=str(data["reservation_id"]),
            hotel_id=str(data["hotel_id"]),
            customer_id=str(data["customer_id"]),
            room=int(data["room"]),
        )

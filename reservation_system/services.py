"""Business logic for managing hotels, customers, and reservations."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from reservation_system.models import Customer, Hotel, Reservation
from reservation_system.storage import load_list, save_list


class ReservationSystem:
    """Business logic for hotels, customers,
    and reservations with JSON persistence."""

    def __init__(self, data_dir: str = "data") -> None:
        self.data_dir = Path(data_dir)
        self.hotels_path = self.data_dir / "hotels.json"
        self.customers_path = self.data_dir / "customers.json"
        self.reservations_path = self.data_dir / "reservations.json"

    # ---------- Helpers ----------
    def _load_hotels(self) -> list[Hotel]:
        return [Hotel.from_dict(x) for x in load_list(self.hotels_path)]

    def _save_hotels(self, hotels: list[Hotel]) -> None:
        save_list(self.hotels_path, [h.to_dict() for h in hotels])

    def _load_customers(self) -> list[Customer]:
        return [Customer.from_dict(x) for x in load_list(self.customers_path)]

    def _save_customers(self, customers: list[Customer]) -> None:
        save_list(self.customers_path, [c.to_dict() for c in customers])

    def _load_reservations(self) -> list[Reservation]:
        return [
            Reservation.from_dict(x) for x in load_list(
                self.reservations_path)]

    def _save_reservations(self, reservations: list[Reservation]) -> None:
        save_list(self.reservations_path, [r.to_dict() for r in reservations])

    @staticmethod
    def _require_non_empty(value: Any, name: str) -> str:
        text = str(value).strip()
        if not text:
            raise ValueError(f"{name} cannot be empty.")
        return text

    @staticmethod
    def _require_positive_int(value: Any, name: str) -> int:
        try:
            number = int(value)
        except (TypeError, ValueError) as exc:
            raise ValueError(f"{name} must be an integer.") from exc
        if number <= 0:
            raise ValueError(f"{name} must be > 0.")
        return number

    # ---------- Hotel operations ----------
    def create_hotel(self, hotel: Hotel) -> None:
        """Create a new hotel."""
        self._require_non_empty(hotel.hotel_id, "hotel_id")
        self._require_non_empty(hotel.name, "name")
        self._require_non_empty(hotel.location, "location")
        _ = self._require_positive_int(hotel.rooms, "rooms")

        hotels = self._load_hotels()
        if any(h.hotel_id == hotel.hotel_id for h in hotels):
            raise ValueError("Hotel ID already exists.")

        hotels.append(hotel)
        self._save_hotels(hotels)

    def delete_hotel(self, hotel_id: str) -> None:
        """Delete hotel by ID (and its reservations)."""
        hotel_id = self._require_non_empty(hotel_id, "hotel_id")

        hotels = self._load_hotels()
        new_hotels = [h for h in hotels if h.hotel_id != hotel_id]
        if len(new_hotels) == len(hotels):
            raise ValueError("Hotel not found.")

        reservations = self._load_reservations()
        reservations = [r for r in reservations if r.hotel_id != hotel_id]

        self._save_hotels(new_hotels)
        self._save_reservations(reservations)

    def display_hotel_info(self, hotel_id: str) -> Hotel:
        """Return hotel info."""
        hotel_id = self._require_non_empty(hotel_id, "hotel_id")
        for hotel in self._load_hotels():
            if hotel.hotel_id == hotel_id:
                return hotel
        raise ValueError("Hotel not found.")

    def modify_hotel_information(
        self,
        hotel_id: str,
        name: str | None = None,
        rooms: int | None = None,
        location: str | None = None,
    ) -> None:
        """Modify hotel fields."""
        hotel_id = self._require_non_empty(hotel_id, "hotel_id")

        hotels = self._load_hotels()
        for i, hotel in enumerate(hotels):
            if hotel.hotel_id != hotel_id:
                continue

            data = hotel.to_dict()
            if name is not None:
                data["name"] = self._require_non_empty(name, "name")
            if rooms is not None:
                data["rooms"] = self._require_positive_int(
                    rooms, "rooms")
            if location is not None:
                data["location"] = self._require_non_empty(
                    location, "location")

            hotels[i] = Hotel.from_dict(data)
            self._save_hotels(hotels)
            return

        raise ValueError("Hotel not found.")

    # ---------- Customer operations ----------
    def create_customer(self, customer: Customer) -> None:
        """Create a new customer."""
        self._require_non_empty(customer.customer_id, "customer_id")
        self._require_non_empty(customer.name, "name")
        self._require_non_empty(customer.email, "email")

        customers = self._load_customers()
        if any(c.customer_id == customer.customer_id for c in customers):
            raise ValueError("Customer ID already exists.")

        customers.append(customer)
        self._save_customers(customers)

    def delete_customer(self, customer_id: str) -> None:
        """Delete customer by ID (and its reservations)."""
        customer_id = self._require_non_empty(customer_id, "customer_id")

        customers = self._load_customers()
        new_customers = [c for c in customers if c.customer_id != customer_id]
        if len(new_customers) == len(customers):
            raise ValueError("Customer not found.")

        reservations = self._load_reservations()
        reservations = [
            r for r in reservations if r.customer_id != customer_id]

        self._save_customers(new_customers)
        self._save_reservations(reservations)

    def display_customer_info(self, customer_id: str) -> Customer:
        """Return customer info."""
        customer_id = self._require_non_empty(customer_id, "customer_id")
        for customer in self._load_customers():
            if customer.customer_id == customer_id:
                return customer
        raise ValueError("Customer not found.")

    def modify_customer_information(
        self,
        customer_id: str,
        name: str | None = None,
        email: str | None = None,
    ) -> None:
        """Modify customer fields."""
        customer_id = self._require_non_empty(customer_id, "customer_id")

        customers = self._load_customers()
        for i, customer in enumerate(customers):
            if customer.customer_id != customer_id:
                continue

            data = customer.to_dict()
            if name is not None:
                data["name"] = self._require_non_empty(name, "name")
            if email is not None:
                data["email"] = self._require_non_empty(email, "email")

            customers[i] = Customer.from_dict(data)
            self._save_customers(customers)
            return

        raise ValueError("Customer not found.")

    # ---------- Reservation operations ----------
    def create_reservation(self, reservation: Reservation) -> None:
        """Create a reservation if possible."""
        self._require_non_empty(reservation.reservation_id, "reservation_id")
        self._require_non_empty(reservation.hotel_id, "hotel_id")
        self._require_non_empty(reservation.customer_id, "customer_id")
        room = self._require_positive_int(reservation.room, "room")

        hotels = self._load_hotels()
        customers = self._load_customers()
        reservations = self._load_reservations()

        hotel = next((
            h for h in hotels if h.hotel_id == reservation.hotel_id), None)
        if hotel is None:
            raise ValueError("Hotel not found.")

        customer_exists = any(
            c.customer_id == reservation.customer_id for c in customers)
        if not customer_exists:
            raise ValueError("Customer not found.")

        if room > hotel.rooms:
            raise ValueError("Room exceeds hotel's room capacity.")

        if any(
                r.reservation_id == reservation.reservation_id
                for r in reservations):
            raise ValueError("Reservation ID already exists.")

        if any(
                r.hotel_id == reservation.hotel_id
                and r.room == room for r in reservations):
            raise ValueError("Room already reserved.")

        reservations.append(reservation)
        self._save_reservations(reservations)

    def cancel_reservation(self, reservation_id: str) -> None:
        """Cancel reservation by ID."""
        reservation_id = self._require_non_empty(
            reservation_id, "reservation_id")

        reservations = self._load_reservations()
        new_reservations = [
            r for r in reservations if r.reservation_id != reservation_id]
        if len(new_reservations) == len(reservations):
            raise ValueError("Reservation not found.")

        self._save_reservations(new_reservations)

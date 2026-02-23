"""Command-line interface for the Reservation System."""
from __future__ import annotations

from reservation_system.models import Customer, Hotel, Reservation
from reservation_system.services import ReservationSystem


def _menu() -> None:
    print("\n=== Reservation System ===")
    print("1) Create hotel")
    print("2) Create customer")
    print("3) Create reservation")
    print("4) Cancel reservation")
    print("5) Display hotel info")
    print("6) Display customer info")
    print("0) Exit")


def main() -> None:
    """Run the interactive command-line reservation system."""
    system = ReservationSystem("data")

    while True:
        _menu()
        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":
                hotel_id = input("Hotel ID: ").strip()
                name = input("Hotel name: ").strip()
                rooms = int(input("Rooms (int): ").strip())
                location = input("Location: ").strip()
                system.create_hotel(Hotel(hotel_id, name, rooms, location))
                print("Hotel created.")

            elif choice == "2":
                customer_id = input("Customer ID: ").strip()
                name = input("Customer name: ").strip()
                email = input("Email: ").strip()
                system.create_customer(Customer(customer_id, name, email))
                print("Customer created.")

            elif choice == "3":
                reservation_id = input("Reservation ID: ").strip()
                hotel_id = input("Hotel ID: ").strip()
                customer_id = input("Customer ID: ").strip()
                room = int(input("Room (int): ").strip())
                system.create_reservation(Reservation(reservation_id, hotel_id, customer_id, room))
                print("Reservation created.")

            elif choice == "4":
                reservation_id = input("Reservation ID to cancel: ").strip()
                system.cancel_reservation(reservation_id)
                print("Reservation cancelled.")

            elif choice == "5":
                hotel_id = input("Hotel ID: ").strip()
                hotel = system.display_hotel_info(hotel_id)
                print(hotel)

            elif choice == "6":
                customer_id = input("Customer ID: ").strip()
                customer = system.display_customer_info(customer_id)
                print(customer)

            elif choice == "0":
                print("Bye!")
                break

            else:
                print("Invalid option.")

        except ValueError as exc:
            print(f"ERROR: {exc}")


if __name__ == "__main__":
    main()

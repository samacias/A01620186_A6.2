import tempfile
import unittest
from pathlib import Path

from reservation_system.models import Customer, Hotel, Reservation
from reservation_system.services import ReservationSystem
from reservation_system.storage import save_list


class TestReservationSystem(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.data_dir = Path(self.tmp.name)

        # Create empty JSON files for each test (assignment note)
        save_list(self.data_dir / "hotels.json", [])
        save_list(self.data_dir / "customers.json", [])
        save_list(self.data_dir / "reservations.json", [])

        self.system = ReservationSystem(str(self.data_dir))

    def tearDown(self):
        self.tmp.cleanup()

    def test_create_hotel_success(self):
        hotel = Hotel("H1", "Hotel Uno", 5, "CDMX")
        self.system.create_hotel(hotel)
        saved = self.system.display_hotel_info("H1")
        self.assertEqual(saved.hotel_id, "H1")

    def test_create_hotel_duplicate_fails(self):
        hotel = Hotel("H1", "Hotel Uno", 5, "CDMX")
        self.system.create_hotel(hotel)
        with self.assertRaises(ValueError):
            self.system.create_hotel(hotel)

    def test_create_customer_success(self):
        customer = Customer("C1", "Ana", "ana@mail.com")
        self.system.create_customer(customer)
        saved = self.system.display_customer_info("C1")
        self.assertEqual(saved.customer_id, "C1")

    def test_create_reservation_success(self):
        self.system.create_hotel(Hotel("H1", "Hotel Uno", 5, "CDMX"))
        self.system.create_customer(Customer("C1", "Ana", "ana@mail.com"))

        reservation = Reservation("R1", "H1", "C1", 1)
        self.system.create_reservation(reservation)

        # reservation saved => cancel should work
        self.system.cancel_reservation("R1")

    def test_reservation_room_already_reserved_fails(self):
        self.system.create_hotel(Hotel("H1", "Hotel Uno", 5, "CDMX"))
        self.system.create_customer(Customer("C1", "Ana", "ana@mail.com"))

        self.system.create_reservation(Reservation("R1", "H1", "C1", 1))
        with self.assertRaises(ValueError):
            self.system.create_reservation(Reservation("R2", "H1", "C1", 1))

    def test_reservation_hotel_not_found_fails(self):
        self.system.create_customer(Customer("C1", "Ana", "ana@mail.com"))
        with self.assertRaises(ValueError):
            self.system.create_reservation(Reservation("R1", "H999", "C1", 1))

    def test_reservation_customer_not_found_fails(self):
        self.system.create_hotel(Hotel("H1", "Hotel Uno", 5, "CDMX"))
        with self.assertRaises(ValueError):
            self.system.create_reservation(Reservation("R1", "H1", "C999", 1))

    def test_cancel_reservation(self) -> None:
        reservation = Reservation("r1", "h1", "c1", 1)
        self.system.create_reservation(reservation)
        self.system.cancel_reservation("r1")
        with self.assertRaises(ValueError):
            self.system.cancel_reservation("r1")

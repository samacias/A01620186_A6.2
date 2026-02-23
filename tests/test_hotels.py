import tempfile
import unittest
from pathlib import Path

from reservation_system.models import Hotel
from reservation_system.services import ReservationSystem


class TestHotels(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.data_dir = Path(self.tmp.name)
        self.system = ReservationSystem(str(self.data_dir))

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_create_and_display_hotel(self) -> None:
        hotel = Hotel("h1", "Hotel One", 10, "MX")
        self.system.create_hotel(hotel)

        loaded = self.system.display_hotel_info("h1")
        self.assertEqual(loaded.hotel_id, "h1")
        self.assertEqual(loaded.name, "Hotel One")

    def test_modify_hotel(self) -> None:
        hotel = Hotel("h1", "Hotel", 10, "MX")
        self.system.create_hotel(hotel)

        self.system.modify_hotel_information("h1", name="New Hotel")

        updated = self.system.display_hotel_info("h1")
        self.assertEqual(updated.name, "New Hotel")

    def test_delete_hotel(self) -> None:
        hotel = Hotel("h1", "Hotel", 10, "MX")
        self.system.create_hotel(hotel)

        self.system.delete_hotel("h1")

        with self.assertRaises(ValueError):
            self.system.display_hotel_info("h1")

    def test_create_hotel_invalid_rooms(self) -> None:
        with self.assertRaises(ValueError):
            self.system.create_hotel(Hotel("h2", "Bad", -1, "MX"))
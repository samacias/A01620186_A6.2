import tempfile
import unittest
from pathlib import Path

from reservation_system.models import Customer
from reservation_system.services import ReservationSystem


class TestCustomers(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.data_dir = Path(self.tmp.name)
        self.system = ReservationSystem(str(self.data_dir))

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_create_and_display_customer(self) -> None:
        customer = Customer("c1", "Ana", "a@test.com")
        self.system.create_customer(customer)

        loaded = self.system.display_customer_info("c1")
        self.assertEqual(loaded.customer_id, "c1")
        self.assertEqual(loaded.name, "Ana")

    def test_modify_customer(self) -> None:
        customer = Customer("c1", "Ana", "a@test.com")
        self.system.create_customer(customer)

        self.system.modify_customer_information("c1", name="Ana2")

        updated = self.system.display_customer_info("c1")
        self.assertEqual(updated.name, "Ana2")

    def test_delete_customer(self) -> None:
        customer = Customer("c1", "Ana", "a@test.com")
        self.system.create_customer(customer)

        self.system.delete_customer("c1")

        with self.assertRaises(ValueError):
            self.system.display_customer_info("c1")

    def test_create_customer_empty_name(self) -> None:
        with self.assertRaises(ValueError):
            self.system.create_customer(Customer("c2", "", "x@test.com"))
        
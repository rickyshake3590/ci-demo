import unittest
from duckfine import DuckFine


class TestDuckFineInit(unittest.TestCase):
    def test_member_id_is_stored(self):
        duck_fine = DuckFine("M001")
        self.assertEqual(duck_fine.member_id, "M001")

    def test_total_owed_initializes_to_zero(self):
        duck_fine = DuckFine("M001")
        self.assertEqual(duck_fine.total_owed, 0.0)


class TestDuckFineCharge(unittest.TestCase):
    def setUp(self):
        self.duck_fine = DuckFine("M001")

    def test_no_charge_within_grace_period_zero_days(self):
        fee = self.duck_fine.charge(0)
        self.assertEqual(fee, 0.0)

    def test_no_charge_within_grace_period_one_day(self):
        fee = self.duck_fine.charge(1)
        self.assertEqual(fee, 0.0)

    def test_no_charge_within_grace_period_two_days(self):
        fee = self.duck_fine.charge(2)
        self.assertEqual(fee, 0.0)

    def test_charge_one_day_after_grace_period(self):
        fee = self.duck_fine.charge(3)
        self.assertEqual(fee, 0.50)

    def test_charge_multiple_days_after_grace_period(self):
        fee = self.duck_fine.charge(5)
        self.assertEqual(fee, 1.50)

    def test_deluxe_flag_doubles_fee(self):
        fee = self.duck_fine.charge(5, deluxe=True)
        self.assertEqual(fee, 3.00)

    def test_deluxe_flag_with_grace_period_days(self):
        fee = self.duck_fine.charge(2, deluxe=True)
        self.assertEqual(fee, 0.0)

    def test_fee_capped_at_max_fee(self):
        fee = self.duck_fine.charge(20)
        self.assertEqual(fee, 5.00)

    def test_deluxe_fee_capped_at_max_fee(self):
        fee = self.duck_fine.charge(20, deluxe=True)
        self.assertEqual(fee, 5.00)

    def test_negative_days_late_raises_error(self):
        with self.assertRaises(ValueError):
            self.duck_fine.charge(-1)

    def test_total_owed_accumulates_charges(self):
        self.duck_fine.charge(3)
        self.duck_fine.charge(5)
        self.assertEqual(self.duck_fine.total_owed, 2.00)

    def test_total_owed_accumulates_with_deluxe(self):
        self.duck_fine.charge(3)
        self.duck_fine.charge(5, deluxe=True)
        self.assertEqual(self.duck_fine.total_owed, 3.50)

    def test_charge_return_value_added_to_total_owed(self):
        fee = self.duck_fine.charge(4)
        self.assertEqual(self.duck_fine.total_owed, fee)

    def test_multiple_charges_accumulate_correctly(self):
        fee1 = self.duck_fine.charge(3)
        fee2 = self.duck_fine.charge(4)
        fee3 = self.duck_fine.charge(5)
        self.assertEqual(self.duck_fine.total_owed, fee1 + fee2 + fee3)


if __name__ == "__main__":
    unittest.main()

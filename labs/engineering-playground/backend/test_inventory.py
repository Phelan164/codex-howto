import unittest

from inventory import reserve


class ReserveTest(unittest.TestCase):
    def test_reserves_available_stock(self) -> None:
        self.assertEqual(reserve(5, 2), 3)

    def test_rejects_quantity_above_stock(self) -> None:
        with self.assertRaisesRegex(ValueError, "insufficient stock"):
            reserve(2, 3)


if __name__ == "__main__":
    unittest.main()

import unittest

from sqlalchemy import inspect

from backend.database.init_db import init_db


class DatabaseInitTests(unittest.TestCase):
    def test_init_db_creates_stocks_table(self):
        init_db()
        inspector = inspect(init_db.__globals__["engine"])
        self.assertTrue(inspector.has_table("stocks"))


if __name__ == "__main__":
    unittest.main()

import unittest
import athrank.db

class TestImporter(unittest.TestCase):
    def test_constructor(self):
        db = athrank.db.DB()
        self.assertIsInstance(db, athrank.db.DB)

    def test_store(self):
        db = athrank.db.DB()
        store = db.store
        self.assertEqual(str(type(store).__name__), 'Store')

    def test_relations(self):
        a = athrank.db.Athlete()
        s = athrank.db.Section()
        c = athrank.db.Category()

if __name__ == '__main__':
    unittest.main()

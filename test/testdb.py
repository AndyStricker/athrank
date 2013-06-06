import unittest
import jugi.db

class TestImporter(unittest.TestCase):
    def test_constructor(self):
        db = jugi.db.DB()
        self.assertIsInstance(db, jugi.db.DB)

    def test_store(self):
        db = jugi.db.DB()
        store = db.store
        self.assertEqual(str(type(store).__name__), 'Store')

    def test_relations(self):
        a = jugi.db.Athlete()
        s = jugi.db.Section()
        c = jugi.db.Category()

if __name__ == '__main__':
    unittest.main()

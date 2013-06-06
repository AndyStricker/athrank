import unittest
import jugi.importer

class TestImporter(unittest.TestCase):
    def test_constructor(self):
        self.assertRaises(TypeError, jugi.importer.CSVImporter)
        self.assertRaises(AttributeError, jugi.importer.CSVImporter, None)

if __name__ == '__main__':
    unittest.main()

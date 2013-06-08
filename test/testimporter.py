import unittest
import athrank.importer

class TestImporter(unittest.TestCase):
    def test_constructor(self):
        self.assertRaises(TypeError, athrank.importer.CSVImporter)
        self.assertRaises(AttributeError, athrank.importer.CSVImporter, None)

if __name__ == '__main__':
    unittest.main()

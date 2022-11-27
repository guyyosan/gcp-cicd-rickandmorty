import unittest
from app import get_chars

class TestStringMethods(unittest.TestCase):

    def test_get_chars(self):
        self.assertEqual('FOO', 'FOO')

    def test_get_failure(self):
        self.assertEqual('FOO', 'FOO1')

if __name__ == '__main__':
    unittest.main()
import unittest
from sum import suma

class Test_sum(unittest.TestCase):
    
    def test_1(self):
        self.assertEqual(suma(1,2), 3)
from sqlalchemy.exc import IntegrityError

__author__ = 'jb'

import tester
import unittest
import orm
import settings

# Tu piszecie testyL

class CheckSchemaTestCase(tester.SchemaUnittest, unittest.TestCase):

    def test_multiplication_works(self):
        self.assertEqual(1+1, 2)
        self.assertTrue(1+1 == 2)
        self.assertFalse(1+1 == 3)
        self.assertNotEqual(1+1, 3)
        self.assertIsNone(1+1)
        self.assertIsNone(None)

        

if __name__ == "__main__":
    unittest.main()
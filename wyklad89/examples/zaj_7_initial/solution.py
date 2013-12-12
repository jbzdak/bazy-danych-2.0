from sqlalchemy.exc import IntegrityError

__author__ = 'jb'

import tester
import unittest
import orm
import settings

class CheckSchemaTestCase(tester.SchemaUnittest, unittest.TestCase):

    def test_create_student(self):
        s = orm.Student(name="Jacek", surname="Bzdak", gender=0, status="status:doktorant", message="foo")
        sess = settings.Session()
        try:
            sess.add(s)
            sess.commit()
        finally:
            sess.close()
        self.assertIsNotNone(s.id)


    def test_multiplication_works(self):
        self.assertEqual(1+1, 2)
        self.assertTrue(1+1 == 2)
        self.assertFalse(1+1 == 3)
        self.assertNotEqual(1+1, 3)
        self.assertIsNone(1+1)
        self.assertIsNone(None)

    def test_create_student_empty_name(self):
        """


        """
        raised_exception = False
        sess = settings.Session()
        try:
            sess.add(orm.Student(name=None, surname="Bzdak", gender=0, status="status:doktorant", message="foo"))
            sess.commit()
        except IntegrityError:
            raised_exception = True
        finally:
            sess.close()

        self.assertTrue(raised_exception)




if __name__ == "__main__":
    unittest.main()
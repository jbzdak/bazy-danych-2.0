# coding=utf-8
import unittest

class TestMathematics(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print(u"SetUp wykonywany raz: Ustawiam matematyczne środowisko")

    def setUp(self):
        print(u"SetUp przed każdym testem: Ustawiam matematyczne środowisko")

    def test_addition(self):
        print("test_addition")
        value = 1 + 1
        self.assertEqual(2, value, u"Dodawanie nie działa")

    def test_substraction(self):
        print("test_substraction")
        value = 1 - 1
        self.assertEqual(0, value, u"Odejmowanie nie działa")

    def tearDown(self):
        print(u"Tear down po każdym teście!")

    @classmethod
    def tearDownClass(cls):
        print(u"Tear down raz!")





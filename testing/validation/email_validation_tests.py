import unittest
from email_validation import email_validation_check


class EmailValidationTestCase(unittest.TestCase):
    def test_email_validation_check(self):
        # False 기대
        self.assertFalse(email_validation_check("#@c#o@gmail*cm"))

        # True 기대
        self.assertTrue(email_validation_check("isi.cho@gmail.com"))

import unittest
from models.prisoner import Prisoner
from models.criminal_record import CriminalRecord
from datetime import datetime

from models.сountry import Country


class TestQualifiedAssociation(unittest.TestCase):

    def setUp(self):
        # Setup common resources for each test
        self.country = Country(name='Poland', capital='Warsaw')
        self.crim_record = CriminalRecord(name='Pirate', id=1)
        self.prisoner = Prisoner(
            name='Mikel',
            nickname='Torrent',
            surname='Dean',
            birth_date=datetime(1999, 5, 17),
            country=self.country,
            criminal_records={}
        )
        self.record_key = f"{self.crim_record.name}_{self.crim_record.id}"
        self.prisoner.add_criminal_record(self.crim_record)

    def test_add_and_retrieve_criminal_record(self):
        """Testing addition and retrieval of a criminal record"""
        self.assertIn(self.record_key, self.prisoner.criminal_records)
        self.assertEqual(self.prisoner.criminal_records[self.record_key], self.crim_record)

    def test_criminal_record_immutability(self):
        """Testing immutability of name in criminal record"""
        with self.assertRaises(ValueError):
            self.crim_record.name = "New Record Name"

    def test_remove_criminal_record(self):
        """Testing removal of a criminal record"""
        self.prisoner.remove_criminal_record(self.record_key)
        self.assertNotIn(self.record_key, self.prisoner.criminal_records)

if __name__ == '__main__':
    unittest.main()

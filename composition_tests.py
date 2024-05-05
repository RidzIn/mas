import unittest
from datetime import datetime

from models.criminal_record import CriminalRecord
from models.prisoner import Prisoner
from models.health_record import HealthRecord
from models.сountry import Country


class TestPrisonerHealthRecordComposition(unittest.TestCase):
    crim_record = CriminalRecord(name='Pirate')
    country = Country(name='Poland', capital='Warsaw')
    prisoner_data = {
        'name': 'Mikel',
        'nickname': 'Torrent',
        'surname': 'Dean',
        'birth_date': datetime(1999, 5, 17),
        'country': country,
        'health_record': {
            'health_conditions': 'Good',
            'last_checkup_date': datetime.now()
        },
        'criminal_records': {}
    }

    def test_health_record_creation(self):
        prisoner = Prisoner(**self.prisoner_data)
        prisoner.add_criminal_record(self.crim_record)

        """Test that a HealthRecord is created with a Prisoner."""
        self.assertIsInstance(prisoner.health_record, HealthRecord, "HealthRecord should be created with Prisoner")

    def test_health_record_unique_to_prisoner(self):
        """Test that the HealthRecord is unique to the Prisoner."""
        prisoner = Prisoner(**self.prisoner_data)
        prisoner.add_criminal_record(self.crim_record)

        another_prisoner = Prisoner(**self.prisoner_data)
        self.assertNotEqual(prisoner.health_record, another_prisoner.health_record,
                            "Each prisoner should have a unique HealthRecord")

    def test_health_record_deletion_with_prisoner(self):
        """Test that deleting a Prisoner also deletes the HealthRecord and updates collection sizes."""

        prisoner = Prisoner(**self.prisoner_data)
        prisoner.add_criminal_record(self.crim_record)

        initial_prisoner_count = len(Prisoner.get_prisoners())
        initial_health_record_count = len(HealthRecord.get_health_records())

        Prisoner.delete_item(item=prisoner)



        self.assertEqual(len(Prisoner.get_prisoners()), initial_prisoner_count - 1, "Prisoner count should decrease by 1")
        self.assertEqual(len(HealthRecord.get_health_records()), initial_health_record_count - 1,
                         "HealthRecord count should decrease by 1")


if __name__ == '__main__':
    unittest.main()

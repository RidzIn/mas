import unittest
from datetime import datetime

from models.criminal_record import CriminalRecord
from models.jail_cell import JailCell
from models.prisoner import Prisoner
from models.сountry import Country


class TestJailCellAssociation(unittest.TestCase):

    country = Country(name='Poland', capital='Warsaw')
    criminal_record = CriminalRecord(name='Pirate')
    prisoner_dict = {
        'name': 'Mikel',
        'nickname': 'Torrent',
        'surname': 'Dean',
        'birth_date': datetime(1999, 5, 17),
        'country': country,
        'criminal_record': [criminal_record]
    }

    def test_add_prisoner_to_cell(self):
        """Test adding prisoners to a jail cell."""
        cell = JailCell()
        prisoners = [Prisoner(**self.prisoner_dict) for _ in range(8)]
        for prisoner in prisoners:
            cell.add_prisoner(prisoner)
            self.assertIn(prisoner, cell.prisoners)

        # Check that the cell does not exceed its capacity
        self.assertRaises(ValueError, cell.add_prisoner, Prisoner(**self.prisoner_dict))

    def test_remove_prisoner_from_cell(self):
        """Test removing prisoners from a jail cell."""
        cell = JailCell()
        prisoner = Prisoner(**self.prisoner_dict)
        cell.add_prisoner(prisoner)
        cell.remove_prisoner(prisoner)
        self.assertNotIn(prisoner, cell.prisoners)

    def test_cell_prisoner_limits(self):
        """Test the limits on the number of prisoners per cell."""
        cell = JailCell()
        prisoners = [Prisoner(**self.prisoner_dict) for _ in range(8)]
        for prisoner in prisoners:
            cell.add_prisoner(prisoner)

        # Try to add one more prisoner beyond limit
        with self.assertRaises(ValueError):
            cell.add_prisoner(Prisoner(id=9))

    def test_prisoner_added_to_cell(self):
        cell = JailCell()
        prisoner = Prisoner(**self.prisoner_dict)
        cell.add_prisoner(prisoner)
        self.assertIn(prisoner, cell.prisoners)
        self.assertEqual(prisoner.jail_cell, cell)

    def test_prisoner_removed_from_cell(self):
        cell = JailCell()
        prisoner = Prisoner(**self.prisoner_dict)
        cell.add_prisoner(prisoner)
        cell.remove_prisoner(prisoner)
        self.assertNotIn(prisoner, cell.prisoners)
        self.assertIsNone(prisoner.jail_cell)


if __name__ == '__main__':
    unittest.main()

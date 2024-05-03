import unittest

from models.criminal_record import CriminalRecord
from models.shift import Shift
from models.guard import Guard
from models.prisoner import Prisoner
from datetime import datetime

from models.сountry import Country


class TestShift(unittest.TestCase):
    country = Country(name='Poland', capital='Warsaw')
    crim_record = CriminalRecord(name='Pirate')
    prisoner_dict = {
        'name': 'Mikel',
        'nickname': 'Torrent',
        'surname': 'Dean',
        'birth_date': datetime(1999, 5, 17),
        'country': country,
        'criminal_records': {}
    }

    def test_no_direct_association(self):
        """Ensure there are no direct links between Guard and Prisoner."""
        guard = Guard()
        prisoner = Prisoner(**self.prisoner_dict)
        prisoner.add_criminal_record(self.crim_record)
        self.assertFalse(hasattr(guard, 'prisoners'))
        self.assertFalse(hasattr(prisoner, 'guards'))

    def test_valid_shift_creation(self):
        """Test shift creation with valid guard and prisoner counts."""
        guards = [Guard() for _ in range(5)]
        prisoners = [Prisoner(**self.prisoner_dict) for _ in range(20)]
        shift = Shift(guards=guards, prisoners=prisoners)
        self.assertEqual(len(shift.guards), 5)
        self.assertEqual(len(shift.prisoners), 20)

    def test_exceed_guard_limit(self):
        """Test creating a shift with more guards than allowed should raise ValueError."""
        guards = [Guard() for _ in range(6)]
        prisoners = [Prisoner(**self.prisoner_dict) for _ in range(20)]
        with self.assertRaises(ValueError):
            Shift(guards=guards, prisoners=prisoners)

    def test_exceed_prisoner_limit(self):
        """Test creating a shift with more prisoners than allowed should raise ValueError."""
        guards = [Guard() for _ in range(5)]
        prisoners = [Prisoner(**self.prisoner_dict) for _ in range(21)]
        with self.assertRaises(ValueError):
            Shift(guards=guards, prisoners=prisoners)

    def test_shift_deletion(self):
        """Test the deletion of a shift removes it from associated guards and prisoners."""
        guards = [Guard() for _ in range(5)]
        prisoners = [Prisoner(**self.prisoner_dict) for _ in range(20)]
        shift = Shift(guards=guards, prisoners=prisoners)
        shift.delete_shift()
        for guard in guards:
            self.assertNotIn(shift, guard.shifts)
        for prisoner in prisoners:
            self.assertNotIn(shift, prisoner.shifts)


if __name__ == '__main__':
    unittest.main()

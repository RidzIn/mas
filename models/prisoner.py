from typing import List, ClassVar, Dict

from pydantic import BaseModel, PrivateAttr
from datetime import datetime, timedelta
from typing import Optional

from utils.collection_manager import CollectionManager
from utils.decorators import validate_string
from utils.serialize_manager import Serializable
from models.сountry import Country
from models.criminal_record import CriminalRecord
from models.jail_cell import JailCell


class PrisonerCounter:
    counter: int = 0

    current_counter: int

    def __init__(self):
        self.current_counter = PrisonerCounter.counter
        PrisonerCounter.counter += 1


class Prisoner(BaseModel, CollectionManager['Prisoner'], Serializable):
    _id: int = PrivateAttr()
    _name: str = PrivateAttr()
    _nickname: Optional[str] = PrivateAttr(default=None)
    _surname: str = PrivateAttr()

    _birth_date: datetime = PrivateAttr()
    _country: Country = PrivateAttr()

    _prisoners: ClassVar[List['Prisoner']] = []
    _criminal_records: Dict[str, 'CriminalRecord'] = {}

    jail_cell: Optional['JailCell'] = None

    shifts: List[object] = []


    def __init__(self, **data):
        super().__init__(**data)
        self._id = PrisonerCounter().counter
        self.name = data.get('name')
        self.nickname = data.get('nickname')
        self.surname = data.get('surname')
        self.birth_date = data.get('birth_date')
        self.country = data.get('country')

        for v in data.get('criminal_records'):
            self.add_criminal_record(v)

        Prisoner.add_item(self)

    @classmethod
    def _get_items(cls) -> List['Prisoner']:
        return cls._prisoners

    @classmethod
    def item_id(cls, item: 'Prisoner') -> int:
        return item._id

    @staticmethod
    def get_file_path(id: int) -> str:
        return f"storage/prisoner_storage/Prisoner_{id}"

    @classmethod
    def get_prisoners(cls) -> List['Prisoner']:
        return cls._prisoners.copy()

    def add_shift(self, shift):
        if shift is None:
            raise ValueError("You can't add None values as shift object")
        if shift not in self.shifts:
            self.shifts.append(shift)
        else:
            raise ValueError("Shift is already assigned to this prisoner")

    def remove_shift(self, shift):
        if shift in self.shifts:
            self.shifts.remove(shift)
        else:
            raise ValueError("Shift not found in this prisoner's list")

    def move_to_cell(self, new_cell: 'JailCell'):
        if new_cell is None:
            raise ValueError("New cell cannot be None")
        if self.jail_cell:
            self.jail_cell.remove_prisoner(self)
        new_cell.add_prisoner(self)

    def leave_cell(self):
        if self.jail_cell:
            self.jail_cell.remove_prisoner(self)
            self.jail_cell = None
        else:
            raise ValueError("Prisoner is not in any cell")


    @property
    def name(self):
        return self._name

    @name.setter
    @validate_string(min_length=3, max_length=50)
    def name(self, value):
        self._name = value

    @property
    def nickname(self) -> Optional[str]:
        return self._nickname

    @nickname.setter
    @validate_string(min_length=1, max_length=50, allow_none=True)
    def nickname(self, value: Optional[str]):
        self._nickname = value

    @property
    def surname(self):
        return self._surname

    @surname.setter
    @validate_string(min_length=3, max_length=50)
    def surname(self, value):
        self._surname = value

    @property
    def birth_date(self):
        return self._birth_date

    @birth_date.setter
    def birth_date(self, value):
        min_age = timedelta(days=14 * 365)
        if datetime.now() - value < min_age:
            raise ValueError("Age must be > 14")
        self._birth_date = value

    @property
    def age(self) -> int:
        today = datetime.now()

        age = today.year - self._birth_date.year
        return age

    @property
    def country(self) -> Country:
        return self._country

    @country.setter
    def country(self, value: Country):
        if value is None:
            raise ValueError('ERROR: value cannot be None')
        if not isinstance(value, Country):
            raise ValueError('ERROR: you provided not an Country object')
        self._country = value

    def __str__(self) -> str:
        return (f"Prisoner(id={self._id}, "
                f"name='{self._name}', "
                f"nick_name='{self._nickname}',"
                f"surname='{self._surname}',"
                f"country='{self._country.__str__()}',"
                f"age='{self.age}',"
                f"birth_date='{self._birth_date}'),"
                f"criminal_records={' '.join([k.__str__()+':'+v.__str__() for k, v in self._criminal_records.items()])}")


    def add_criminal_record(self, record: CriminalRecord):
        if f"{record.name}_{record.id}" in self._criminal_records:
            raise ValueError("You cannot add the same criminal record twice")
        self._criminal_records[f"{record.name}_{record.id}"] = record

    def get_criminal_record(self, record_key: str) -> Optional[CriminalRecord]:
        return self._criminal_records.get(record_key)

    def remove_criminal_record(self, record_key: str):
        if record_key in self._criminal_records:
            del self._criminal_records[record_key]
        else:
            raise ValueError("No record found with this key.")

    @property
    def criminal_records(self) -> Dict[str, CriminalRecord]:
        return self._criminal_records.copy()

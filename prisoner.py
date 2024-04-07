from typing import List, ClassVar

from pydantic import BaseModel, PrivateAttr
import pickle
from datetime import datetime, timedelta
from typing import Optional

from decorators import validate_string
from сountry import Country

from criminal_record import CriminalRecord


def get_file_path(id):
    return f"storage/prisoner_storage/Prisoner_{id}"


class PrisonerCounter:
    counter: int = 0

    current_counter: int

    def __init__(self):
        self.current_counter = PrisonerCounter.counter
        PrisonerCounter.counter += 1


class Prisoner(BaseModel):
    _id: int = PrivateAttr()
    _name: str = PrivateAttr()
    _nickname: Optional[str] = PrivateAttr(default=None)
    _surname: str = PrivateAttr()

    _birth_date: datetime = PrivateAttr()
    _country: Country = PrivateAttr()

    _prisoners: ClassVar[List['Prisoner']] = []
    _criminal_record: List['CriminalRecord']

    def __init__(self, **data):
        super().__init__(**data)
        self._id = PrisonerCounter().counter
        self.name = data.get('name')
        self.nickname = data.get('nickname')
        self.surname = data.get('surname')
        self.birth_date = data.get('birth_date')
        self.country = data.get('country')
        self.criminal_record = data.get('criminal_record')
        Prisoner.add_new_prisoner(self)


    @classmethod
    def add_new_prisoner(cls, prisoner):
        if not isinstance(prisoner, Prisoner):
            raise ValueError('ERROR: prisoners must contain only prisoners object')
        if prisoner in Prisoner._prisoners:
            raise ValueError('ERROR: prisoner already in the list')
        Prisoner._prisoners.append(prisoner)
        print(f'Added: Prisoner {prisoner._id}')

    @classmethod
    def delete_new_prisoner(cls, prisoner_id=None, prisoner=None):
        if prisoner_id is not None and prisoner is not None:
            raise ValueError('ERROR: Please provide either prisoner_id or prisoner, not both.')

        if prisoner_id is None and prisoner is None:
            raise ValueError('ERROR: Please provide either prisoner_id or prisoner.')

        if prisoner_id is not None:
            if not any(p._id == prisoner_id for p in Prisoner._prisoners):
                raise ValueError(f'ERROR: No prisoner found with ID {prisoner_id}')
            Prisoner._prisoners = [p for p in Prisoner._prisoners if p._id != prisoner_id]
            print(f'Deleted: Prisoner {prisoner_id}')

        elif prisoner is not None:
            if prisoner not in Prisoner._prisoners:
                raise ValueError('ERROR: The provided prisoner object is not in the list')
            Prisoner.prisoners = [p for p in Prisoner._prisoners if p is not prisoner]
            print(f'Deleted: Prisoner {prisoner.id}')

    def save_to_pickle(self) -> None:
        try:
            with open(get_file_path(self._id), 'wb') as file:
                pickle.dump(self, file)
                print('Saved:', self.__str__())
        except IOError as e:
            print(f"Error while saving the object: {e}")

    @classmethod
    def load_from_pickle(cls, id: int):
        try:
            with open(get_file_path(id), 'rb') as file:
                instance = pickle.load(file)
                print('Load:', instance.__str__())
            return instance
        except FileNotFoundError as e:
            print(e)
        except pickle.UnpicklingError as e:
            print(e)
        except Exception as e:
            print(e)

    @classmethod
    def get_prisoners(cls) -> List['Prisoner']:
        return cls._prisoners.copy()

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
        self._country = value

    def __str__(self) -> str:
        return (f"Prisoner(id={self._id}, "
                f"name='{self._name}', "
                f"nick_name='{self._nickname}',"
                f"surname='{self._surname}',"
                f"country='{self._country.__str__()}',"
                f"age='{self.age}',"
                f"birth_date='{self._birth_date}'),"
                f"criminal_records={' '.join([record.__str__() for record in self.criminal_record])}")


    @property
    def criminal_record(self):
        return self._criminal_record

    @criminal_record.setter
    def criminal_record(self, value):
        self._criminal_record = value

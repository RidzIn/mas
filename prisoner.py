from typing import List

from pydantic import BaseModel, PrivateAttr
import pickle
from datetime import datetime, timedelta
from typing import Optional

from decorators import validate_string
from сountry import Country


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

    # _criminal_record: List = PrivateAttr()

    def __init__(self, **data):
        super().__init__(**data)
        self._id = PrisonerCounter().counter
        self.name = data.get('name')
        self.nickname = data.get('nickname')
        self.surname = data.get('surname')
        self.birth_date = data.get('birth_date')
        self.country = data.get('country')

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
        min_age = timedelta(days=14*365)
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
        return super().__str__()



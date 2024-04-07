from typing import ClassVar, List

from pydantic import BaseModel, PrivateAttr
from utils.collection_manager import CollectionManager
from utils.decorators import validate_string
from utils.serialize_manager import Serializable


class CountryCounter:
    counter: int = 0

    current_counter: int

    def __init__(self):
        self.current_counter = CountryCounter.counter
        CountryCounter.counter += 1


class Country(BaseModel, CollectionManager['Country'], Serializable):
    _id: int = PrivateAttr()
    _name: str = PrivateAttr()
    _capital: str = PrivateAttr()

    _id_counter: int = 0

    _counties: ClassVar[List['Country']] = []

    def __init__(self, **data):
        super().__init__(**data)
        self._id = CountryCounter().counter
        self.name = data.get('name')
        self.capital = data.get('capital')

        Country.add_item(self)

    @staticmethod
    def get_file_path(id: int) -> str:
        return f"storage/country_storage/Country_{id}"

    @classmethod
    def _get_items(cls) -> List['Country']:
        """Do not call this function outside please (("""
        return cls._counties

    @classmethod
    def item_id(cls, item: 'Country') -> int:
        return item._id

    @classmethod
    def get_counties(cls) -> List['Country']:
        return cls._counties.copy()

    @property
    def name(self):
        return self._name

    @name.setter
    @validate_string(min_length=3, max_length=50)
    def name(self, value):
        self._name = value

    @property
    def capital(self):
        return self._capital

    @capital.setter
    @validate_string(min_length=3, max_length=50)
    def capital(self, value):
        self._capital = value

    @property
    def id(self):
        return self._id

    def __str__(self) -> str:
        return f"Country(id={self._id}, name='{self._name}', capital='{self._capital}')"

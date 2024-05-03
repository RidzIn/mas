from typing import Optional, ClassVar, List

from pydantic import BaseModel, PrivateAttr

from utils.collection_manager import CollectionManager
from utils.decorators import validate_string
from utils.serialize_manager import Serializable


class CriminalRecordCounter:
    counter: int = 0

    current_counter: int

    def __init__(self):
        self.current_counter = CriminalRecordCounter.counter
        CriminalRecordCounter.counter += 1


class CriminalRecord(BaseModel, CollectionManager['CriminalRecord'], Serializable):
    _id: int = PrivateAttr()
    _name: PrivateAttr()
    _description: Optional[str] = PrivateAttr(default=None)

    _id_counter: int = 0

    _criminal_records: ClassVar[List['CriminalRecord']] = []

    def __init__(self, **data):
        super().__init__(**data)
        self._id = CriminalRecordCounter().counter
        self._name = None
        self.name = data.get('name')
        self.description = data.get('description')

        CriminalRecord.add_item(self)

    @staticmethod
    def get_file_path(id: int) -> str:
        return f"storage/criminal_record_storage/CriminalRecord_{id}"

    @classmethod
    def _get_items(cls) -> List['CriminalRecord']:
        return cls._criminal_records

    @classmethod
    def item_id(cls, item: 'CriminalRecord') -> int:
        return item._id

    @classmethod
    def get_criminal_records(cls) -> List['CriminalRecord']:
        return cls._criminal_records.copy()


    @property
    def name(self):
        return self._name

    @name.setter
    @validate_string(min_length=3, max_length=50)
    def name(self, value):
        if self._name is not None:
            raise ValueError("You can't change the name after object was created")
        self._name = value

    @property
    def description(self):
        return self._description

    @description.setter
    @validate_string(min_length=10, max_length=500, pattern="^[A-Za-z0-9 .,-]+$", allow_none=True)
    def description(self, value):
        self._description = value

    @property
    def id(self):
        return self._id

    def __str__(self) -> str:
        return f"Criminal Record(id={self._id}, name='{self._name}', description='{self._description}')"



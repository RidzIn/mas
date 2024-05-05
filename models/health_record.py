from datetime import datetime
from typing import ClassVar, List
from pydantic import BaseModel, PrivateAttr
from utils.collection_manager import CollectionManager
from utils.decorators import validate_string
from utils.serialize_manager import Serializable


class HealthRecordCounter:
    counter: int = 0

    def __init__(self):
        self.current_counter = HealthRecordCounter.counter
        HealthRecordCounter.counter += 1


class HealthRecord(BaseModel, CollectionManager['HealthRecord'], Serializable):
    _id: int = PrivateAttr()
    _health_conditions: str = PrivateAttr()
    _last_checkup_date: datetime = PrivateAttr()

    _health_records: ClassVar[List['HealthRecord']] = []

    def __init__(self, **data):
        super().__init__(**data)
        self._id = HealthRecordCounter().counter
        self.health_conditions = data.get('health_conditions')
        self.last_checkup_date = data.get('last_checkup_date')

        HealthRecord.add_item(self)

    @staticmethod
    def get_file_path(id: int) -> str:
        return f"storage/health_record_storage/HealthRecord_{id}"

    @classmethod
    def _get_items(cls) -> List['HealthRecord']:
        return cls._health_records

    @classmethod
    def item_id(cls, item: 'HealthRecord') -> int:
        return item._id

    @classmethod
    def get_health_records(cls) -> List['HealthRecord']:
        return cls._health_records.copy()

    @property
    def health_conditions(self):
        return self._health_conditions

    @health_conditions.setter
    @validate_string(min_length=3, max_length=500, allow_none=False)
    def health_conditions(self, value):
        self._health_conditions = value

    @property
    def last_checkup_date(self):
        return self._last_checkup_date

    @last_checkup_date.setter
    def last_checkup_date(self, value: datetime):
        self._last_checkup_date = value

    @property
    def id(self):
        return self._id

    def __str__(self) -> str:
        return f"Health Record(id={self._id}, conditions='{self._health_conditions}', last_checkup='{self._last_checkup_date}')"

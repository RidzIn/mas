import pickle
from typing import Optional, ClassVar, List

from pydantic import BaseModel, PrivateAttr

from decorators import validate_string


def get_file_path(id):
    return f"storage/criminal_storage/Criminal_record_{id}"


class CriminalRecordCounter:
    counter: int = 0

    current_counter: int

    def __init__(self):
        self.current_counter = CriminalRecordCounter.counter
        CriminalRecordCounter.counter += 1


class CriminalRecord(BaseModel):
    _id: int = PrivateAttr()
    _name: str = PrivateAttr()
    _description: Optional[str] = PrivateAttr(default=None)

    _criminal_records: ClassVar[List['CriminalRecord']] = []

    def __init__(self, **data):
        super().__init__(**data)
        self._id = CriminalRecordCounter().counter
        self.name = data.get('name')
        self.description = data.get('description')

    @classmethod
    def get_prisoners(cls) -> List['CriminalRecord']:
        return cls._criminal_records.copy()

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

    @property
    def name(self):
        return self._name


    @name.setter
    @validate_string(min_length=3, max_length=50)
    def name(self, value):
        self._name = value

    @property
    def description(self):
        return self._description

    @description.setter
    @validate_string(min_length=10, max_length=500, pattern="^[A-Za-z0-9 .,-]+$")
    def description(self, value):
        self._description = value


    def __str__(self) -> str:
        return f"Criminal Record(id={self._id}, name='{self._name}', description='{self._description}')"



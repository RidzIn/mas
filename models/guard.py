from typing import List, ClassVar
from pydantic import BaseModel, PrivateAttr

from utils.collection_manager import CollectionManager
from utils.serialize_manager import Serializable


class GuardCounter:
    counter: int = 0

    current_counter: int

    def __init__(self):
        self.current_counter = GuardCounter.counter
        GuardCounter.counter += 1


class Guard(BaseModel, CollectionManager['Guard'], Serializable):
    _id: int = PrivateAttr()
    _guards: ClassVar[List['Guard']] = []
    shifts: List[object] = []

    def __init__(self):
        super().__init__()
        self._id = GuardCounter().counter
        Guard.add_item(self)

    def add_shift(self, shift):
        from models.shift import Shift
        if shift is None:
            raise ValueError("You can't add None values as a shift object")
        if shift not in self.shifts:
            self.shifts.append(shift)
        else:
            raise ValueError("Shift is already assigned to this guard")

    def remove_shift(self, shift):
        from models.shift import Shift
        if shift in self.shifts:
            self.shifts.remove(shift)
        else:
            raise ValueError("Shift not found in this guard's list")


    @classmethod
    def _get_items(cls) -> List['Guard']:
        return cls._guards

    @classmethod
    def item_id(cls, item: 'Guard') -> int:
        return item._id

    @staticmethod
    def get_file_path(id: int) -> str:
        return f"storage/guard_storage/Guard_{id}"

    @classmethod
    def get_guards(cls) -> List['Guard']:
        return cls._guards.copy()

    def __str__(self) -> str:
        return f'Guard(id={self._id})'


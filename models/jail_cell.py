from typing import List, ClassVar
from pydantic import BaseModel, PrivateAttr

from utils.collection_manager import CollectionManager
from utils.serialize_manager import Serializable


class JailCellCounter:
    counter: int = 0

    current_counter: int

    def __init__(self):
        self.current_counter = JailCellCounter.counter
        JailCellCounter.counter += 1


class JailCell(BaseModel, CollectionManager['JailCell'], Serializable):
    _id: int = PrivateAttr()

    _jail_cells: ClassVar[List['JailCell']] = []

    prisoners: List[object] = []

    def __init__(self):
        super().__init__()
        self._id = JailCellCounter().counter

        JailCell.add_item(self)

    @classmethod
    def _get_items(cls) -> List['JailCell']:
        return cls._jail_cells

    @classmethod
    def item_id(cls, item: 'JailCell') -> int:
        return item._id

    @staticmethod
    def get_file_path(id: int) -> str:
        return f"storage/jail_cell_storage/JailCell_{id}"

    @classmethod
    def get_jail_cells(cls) -> List['JailCell']:
        return cls._jail_cells.copy()


    def __str__(self) -> str:
        return f'JailCell(id={self._id})'

    def add_prisoner(self, prisoner):
        from models.prisoner import Prisoner
        if prisoner is None:
            raise ValueError('Prisoner cannot be None')
        if prisoner not in self.prisoners and len(self.prisoners) < 8:
            self.prisoners.append(prisoner)
            prisoner.jail_cell = self
        elif prisoner in self.prisoners:
            raise ValueError("This prisoner is already in this cell.")
        else:
            raise ValueError("The cell is full.")

    def remove_prisoner(self, prisoner):
        if prisoner in self.prisoners:
            self.prisoners.remove(prisoner)
            prisoner.jail_cell = None
from abc import ABC, abstractmethod
from typing import List, TypeVar, Generic

T = TypeVar('T')


class CollectionManager(ABC, Generic[T]):
    @classmethod
    @abstractmethod
    def _get_items(cls) -> List[T]:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def item_id(cls, item: T) -> int:
        raise NotImplementedError

    @classmethod
    def add_item(cls, item: T) -> None:
        items = cls._get_items()
        if item in items:
            raise ValueError('ERROR: Item already in the list')
        items.append(item)
        print(f'Added: Item {cls.item_id(item)}')

    @classmethod
    def delete_item(cls, item_id: int = None, item: T = None) -> None:
        items = cls._get_items()
        if item_id is not None:
            items[:] = [p for p in items if cls.item_id(p) != item_id]
            print(f'Deleted: Item {item_id}')
        elif item is not None:
            items.remove(item)
            print(f'Deleted: Item {cls.item_id(item)}')

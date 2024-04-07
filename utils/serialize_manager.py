from abc import ABC, abstractmethod
import pickle


class Serializable(ABC):
    @staticmethod
    @abstractmethod
    def get_file_path(id: int) -> str:
        raise NotImplementedError

    def save_to_pickle(self) -> None:
        try:
            with open(self.get_file_path(self._id), 'wb') as file:
                pickle.dump(self, file)
                print(f'Saved: {self}')
        except IOError as e:
            print(f"ERROR: couldn't save the object: {e}")

    @classmethod
    def load_from_pickle(cls, id: int):
        try:
            with open(cls.get_file_path(id), 'rb') as file:
                instance = pickle.load(file)
                print(f'Loaded: {instance}')
            return instance
        except FileNotFoundError as e:
            print(f"ERROR: File not found: {e}")
        except pickle.UnpicklingError as e:
            print(f"ERROR: Unpickling error: {e}")
        except Exception as e:
            print(f"ERROR: An error occurred: {e}")


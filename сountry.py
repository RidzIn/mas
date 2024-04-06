from pydantic import BaseModel, PrivateAttr
import pickle

from decorators import validate_string


def get_file_path(id):
    return f"storage/country_storage/Country_{id}"


class CountryCounter:
    counter: int = 0

    current_counter: int

    def __init__(self):
        self.current_counter = CountryCounter.counter
        CountryCounter.counter += 1


class Country(BaseModel):
    _id: int = PrivateAttr()
    _name: str = PrivateAttr()
    _capital: str = PrivateAttr()

    _id_counter: int = 0

    def __init__(self, **data):
        super().__init__(**data)
        self._id = CountryCounter().counter
        self.name = data.get('name')
        self.capital = data.get('capital')

    def __str__(self) -> str:
        return f"Country(id={self._id}, name='{self._name}', capital='{self._capital}')"

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

    @property
    def capital(self):
        return self._capital

    @property
    def id(self):
        return self._id

    @name.setter
    @validate_string(min_length=3, max_length=50)
    def name(self, value):
        self._name = value

    @capital.setter
    @validate_string(min_length=3, max_length=50)
    def capital(self, value):
        self._capital = value


country1 = Country(name='Poland', capital='Warsaw')
country2 = Country(name='Germany', capital='Berlin')
country3 = Country(name='Ukraine', capital='Kiev')

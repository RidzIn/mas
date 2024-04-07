# import pickle
#
#
# class Pickleable:
#
#     def get_file_path(self) -> str:
#         raise NotImplementedError("Subclasses must implement `get_file_path` method")
#
#     def save_to_pickle(self) -> None:
#         with open(self.get_file_path(), 'wb') as file:
#             pickle.dump(self, file)
#             print(f'Saved: {self}')
#
#     @classmethod
#     def load_from_pickle(cls, id: int):
#         with open(cls.get_file_path(self), 'rb') as file:
#             instance = pickle.load(file)
#             print(f'Loaded: {instance}')
#             return instance


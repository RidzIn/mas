from datetime import datetime

from prisoner import Prisoner
from сountry import Country
from criminal_record import CriminalRecord

# print('\n\n--------------Start of testing the Country class--------------\n\n')
#
# try:
# poland = Country(name='Poland', capital='Warsaw')
#     poland.save_to_pickle()
#     Country.load_from_pickle(1)
# except ValueError as e:
#     print(e)
#
# try:
#     poland = Country(name=1, capital=2)
# except ValueError as e:
#     print(e)
#
# try:
#     poland = Country(name='dd', capital='dd')
# except ValueError as e:
#     print(e)
#
# try:
#     poland = Country(name='df-d', capital='d-d')
# except ValueError as e:
#     print(e)
#
# print('\n\n--------------End of testing the Country class--------------\n\n')
#
#
# prisoner1 = Prisoner(name="Andrei", surname="Chikatilo", birth_date=datetime(1936, 5, 20), country=poland)
# #
# prisoner1.save_to_pickle()
# prisoner2 = Prisoner.load_from_pickle(1)
#
# prisoner2.country.save_to_pickle()
#
# # Prisoner.add_new_prisoner(prisoner2)
#
# Prisoner.delete_new_prisoner(1)
# # Prisoner.delete_new_prisoner(prisoner2)
# temp = Prisoner.get_prisoners()
# print(temp[0])
# temp[0] = None
# print(temp)
# [print(p) for p in Prisoner.get_prisoners()]









# prisoner1 = Prisoner(name="John Doe", surname="Dofe", birth_date=datetime(1980, 5, 20), country=poland)
# prisoner2 = Prisoner(name="Jane Doe", nickname="JJfJ", surname="Dfoe", birth_date=datetime(1990, 8, 15), country=germany)
#
#
# print(prisoner1.name, prisoner1.surname, prisoner1.birth_date, prisoner1.country.name, prisoner1.age)
# print(prisoner2.name, prisoner2.nickname, prisoner2.surname, prisoner2.birth_date, prisoner2.country.name, prisoner2.age)
#
# try:
#     prisoner1.birth_date = datetime(2030, 1, 1)
# except ValueError as e:
#     print(e)
#
# try:
#     prisoner2.name = "Al"
# except ValueError as e:
#     print(e)

criminal_record_1 = CriminalRecord(name='Murder', description='While robbing the shop, killed the cashier')
criminal_record_2 = CriminalRecord(name='Robbery', description='Robbed the shop')

records = [criminal_record_1, criminal_record_2]

poland = Country(name='Poland', capital='Warsaw')

prisoner1 = Prisoner(name="John Doe", surname="Dofe", birth_date=datetime(1980, 5, 20), country=poland, criminal_record=records)

print(prisoner1)


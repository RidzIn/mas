from datetime import datetime

from prisoner import Prisoner
from сountry import Country

poland = Country(name='Poland', capital='Warsaw')
germany = Country(name='Germany', capital='Berlin')
ukraine = Country(name='Ukraine', capital='Kiev')


prisoner1 = Prisoner(name="John Doe", surname="Dofe", birth_date=datetime(1980, 5, 20), country=poland)
prisoner2 = Prisoner(name="Jane Doe", nickname="JJfJ", surname="Dfoe", birth_date=datetime(1990, 8, 15), country=germany)


print(prisoner1.name, prisoner1.surname, prisoner1.birth_date, prisoner1.country.name, prisoner1.age)
print(prisoner2.name, prisoner2.nickname, prisoner2.surname, prisoner2.birth_date, prisoner2.country.name, prisoner2.age)

try:
    prisoner1.birth_date = datetime(2030, 1, 1)
except ValueError as e:
    print(e)

try:
    prisoner2.name = "Al"
except ValueError as e:
    print(e)

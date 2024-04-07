from datetime import datetime

from models.criminal_record import CriminalRecord
from models.prisoner import Prisoner
from models.сountry import Country


def print_collection(collection):
    print('\t' + "\n\t".join(item.__str__() for item in collection))


def country_test():
    poland = Country(name='Poland', capital='Warsaw')
    germany = Country(name='Germany', capital='Berlin')
    ukraine = Country(name='Ukraine', capital='Kiev')

    try:
        country1 = Country(name='000', capital='333')
    except ValueError as e:
        print(e)

    try:
        country2 = Country(name=0, capital='333')
    except ValueError as e:
        print(e)

    print('Testing the collection protection')
    country_list = Country.get_counties()
    print_collection(country_list)
    country_list[0] = None
    print_collection(country_list)
    print_collection(Country.get_counties())

    print('Testing deleting the item by ID')
    Country.delete_item(item_id=1)
    print_collection(Country.get_counties())

    print('Testing deleting the item by object reference')
    Country.delete_item(item=ukraine)
    print_collection(Country.get_counties())

    print('Testing loading and saving object')
    germany.save_to_pickle()
    loaded_object = Country.load_from_pickle(2)
    print(loaded_object)


# country_test()

def criminal_record_test():
    morder = CriminalRecord(name='Murder', description='Murdered the cachier while robbing the shop')
    robber = CriminalRecord(name='Robbery')
    rape = CriminalRecord(name='Rape')

    try:
        criminal_record1 = CriminalRecord(name='000', description='333')
    except ValueError as e:
        print(e)

    try:
        criminal_record2 = CriminalRecord(name=2, description=2)
    except ValueError as e:
        print(e)

    print('Testing the collection protection')
    criminal_record_list = CriminalRecord.get_criminal_records()
    print_collection(criminal_record_list)
    criminal_record_list[0] = None
    print_collection(criminal_record_list)
    print_collection(CriminalRecord.get_criminal_records())


    print('Testing deleting the item by ID')
    CriminalRecord.delete_item(item_id=1)
    print_collection(CriminalRecord.get_criminal_records())

    print('Testing deleting the item by object reference')
    CriminalRecord.delete_item(item=rape)
    print_collection(CriminalRecord.get_criminal_records())

    print('Testing loading and saving object')
    robber.save_to_pickle()
    loaded_object = CriminalRecord.load_from_pickle(2)
    print(loaded_object)

# criminal_record_test()


def prisoner_test():
    country = Country(name='Poland', capital='Warsaw')
    morder = CriminalRecord(name='Murder', description='Murdered the cachier while robbing the shop')
    robber = CriminalRecord(name='Robbery')

    prisoner1 = Prisoner(name='Andrei', surname='Chikatilo', birth_date=datetime(year=1936, day=1, month=1), country=country,
                         criminal_record=[morder, robber])

    prisoner2 = Prisoner(name='Andrei', nickname='savage', surname='Chikatilo', birth_date=datetime(year=1936, day=1, month=1), country=country,
                         criminal_record=[morder, robber])

    prisoner3 = Prisoner(name='Andrei', nickname='savage', surname='Chikatilo',
                         birth_date=datetime(year=1936, day=1, month=1), country=country,
                         criminal_record=[morder, robber])

    print('Testing the collection protection')
    temp = Prisoner.get_prisoners()
    print_collection(temp)
    temp[0] = None
    print_collection(temp)
    print_collection(Prisoner.get_prisoners())


    print('Testing deleting the item by ID')
    Prisoner.delete_item(item_id=2)
    print_collection(Prisoner.get_prisoners())

    print('Testing deleting the item by object reference')
    Prisoner.delete_item(item=prisoner1)
    print_collection(Prisoner.get_prisoners())

    print('Testing loading and saving object')
    prisoner3.save_to_pickle()
    loaded_object = Prisoner.load_from_pickle(3)
    print(loaded_object)


prisoner_test()

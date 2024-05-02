def test_shift_association():
    # Create sample guards and prisoners
    guards = [Guard() for i in range(10)]  # Creating 10 guards
    country = Country(name='fsdfsdfsd', capital='sdfdsfsdf')
    criminal_record = CriminalRecord(name='fdsfsdfsdf')
    prisoners = [Prisoner(name='afdfdsfsdfsdf', nickname='fdsfdsfsdfd', surname='dfdsfdsfsdfs', birth_date=datetime(1999, 5, 17), country=country, criminal_record=[criminal_record]) for _ in range(30)]  # Creating 30 prisoners

    # Test adding too many guards
    try:
        shift_with_too_many_guards = Shift(guards=guards[:6], prisoners=prisoners[:20])
        print("Test failed: No error raised when adding too many guards")
    except ValueError as e:
        print("Test passed: Correctly raised error when adding too many guards:", str(e))

    # Test adding too many prisoners
    try:
        shift_with_too_many_prisoners = Shift(guards=guards[:5], prisoners=prisoners[:21])
        print("Test failed: No error raised when adding too many prisoners")
    except ValueError as e:
        print("Test passed: Correctly raised error when adding too many prisoners:", str(e))
    #
    # Test proper shift creation
    try:
        correct_shift = Shift(guards=guards[:5], prisoners=prisoners[:20])
        print("Test passed: Shift created successfully with correct number of guards and prisoners")
    except ValueError as e:
        print("Test failed: Error raised during correct shift creation:", str(e))


if __name__ == "__main__":
    from models.criminal_record import CriminalRecord
    from models.shift import Shift
    from models.guard import Guard
    from models.prisoner import Prisoner
    from datetime import datetime
    from models.сountry import Country

    test_shift_association()

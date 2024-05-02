from datetime import datetime, timedelta
from typing import List
from pydantic import BaseModel
from models.guard import Guard
from models.prisoner import Prisoner



class Shift(BaseModel):
    start_date: datetime = datetime.now()
    end_date: datetime = datetime.now() + timedelta(hours=8)
    _guards: List[Guard] = []
    _prisoners: List[Prisoner] = []

    def __init__(self, guards: List[Guard], prisoners: List[Prisoner], start_date=None, end_date=None):
        super().__init__()
        self.start_date = datetime.now() if start_date is None else start_date
        self.end_date = self.start_date + timedelta(hours=8) if end_date is None else end_date

        if self.end_date <= self.start_date:
            raise ValueError("end_date must be later than start_date")

        self._guards = guards
        self._prisoners = prisoners

        if not 0 < len(guards) < 6:
            raise ValueError(f"{len(guards)} must be between 1 and 5")
        elif not 0 < len(prisoners) < 21:
            raise ValueError(f"{len(prisoners)} must be between 1 and 20")
        else:
            for guard in guards:
                guard.add_shift(self)
            for prisoner in prisoners:
                prisoner.add_shift(self)

    @property
    def guards(self) -> List['Guard']:
        return self._guards.copy()

    @property
    def prisoners(self) -> List['Prisoner']:
        return self._prisoners.copy()

    def delete_shift(self):
        for guard in self.guards:
            guard.remove_shift(self)
        for prisoner in self.prisoners:
            prisoner.remove_shift(self)
        self.guards.clear()
        self.prisoners.clear()

    def add_guard(self, guard: Guard):
        if guard not in self._guards:
            self._guards.append(guard)
            guard.add_shift(self)  # Ensures the bidirectional link

    def remove_guard(self, guard: Guard):
        if guard in self._guards:
            self._guards.remove(guard)
            guard.remove_shift(self)  # Maintain integrity

    def add_prisoner(self, prisoner: Prisoner):
        if prisoner not in self._prisoners:
            self._prisoners.append(prisoner)
            prisoner.add_shift(self)  # Ensures the bidirectional link

    def remove_prisoner(self, prisoner: Prisoner):
        if prisoner in self._prisoners:
            self._prisoners.remove(prisoner)
            prisoner.remove_shift(self)  # Maintain integrity


    def __str__(self):
        return f"Shift from {self.start_date} to {self.end_date} with Guards: {[guard.id for guard in self.guards]}, Prisoners: {[prisoner.id for prisoner in self.prisoners]}"

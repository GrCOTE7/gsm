from upu.models.habit import Habit
from upu.services.habit_service import HabitService


class HabitController:
    def __init__(self):
        self.service = HabitService()

    def get_habits(self) -> list[Habit]:
        return self.service.get_all()

    def add_habit(self, name: str, frequency: str = "daily") -> Habit:
        habit = Habit(name=name, frequency=frequency)
        self.service.save(habit)
        return habit

    def delete_habit(self, habit_id: int):
        self.service.delete(habit_id)

    def check_in(self, habit_id: int):
        self.service.check_in(habit_id)

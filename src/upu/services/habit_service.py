from upu.models.habit import Habit
from upu.services.db_service import DBService


class HabitService:
    def __init__(self):
        self._db = DBService()
        self._db.init_db()

    def get_all(self) -> list[Habit]:
        return self._db.get_all_habits()

    def save(self, habit: Habit) -> Habit:
        return self._db.save_habit(habit)

    def delete(self, habit_id: int):
        self._db.delete_habit(habit_id)

    def check_in(self, habit_id: int):
        self._db.check_in_habit(habit_id)

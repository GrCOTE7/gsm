import json
import sqlite3
from datetime import date
from pathlib import Path

from upu.models.habit import Habit

DATA_DIR = Path(__file__).resolve().parents[1] / "app_data"
DB_PATH = DATA_DIR / "upu.db"


class DBService:
    def _connect(self):
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        return sqlite3.connect(DB_PATH)

    def init_db(self):
        with self._connect() as con:
            con.execute("""
                CREATE TABLE IF NOT EXISTS habits (
                    id        INTEGER PRIMARY KEY AUTOINCREMENT,
                    name      TEXT NOT NULL,
                    frequency TEXT NOT NULL DEFAULT 'daily',
                    created_at TEXT NOT NULL,
                    checkins  TEXT NOT NULL DEFAULT '[]'
                )
            """)

    def get_all_habits(self) -> list[Habit]:
        with self._connect() as con:
            rows = con.execute(
                "SELECT id, name, frequency, created_at, checkins FROM habits"
            ).fetchall()
        return [
            Habit(
                id=row[0],
                name=row[1],
                frequency=row[2],
                created_at=date.fromisoformat(row[3]),
                checkins=[date.fromisoformat(d) for d in json.loads(row[4])],
            )
            for row in rows
        ]

    def save_habit(self, habit: Habit) -> Habit:
        with self._connect() as con:
            cur = con.execute(
                "INSERT INTO habits (name, frequency, created_at, checkins) VALUES (?, ?, ?, ?)",
                (habit.name, habit.frequency, habit.created_at.isoformat(), "[]"),
            )
            habit.id = cur.lastrowid
        return habit

    def delete_habit(self, habit_id: int):
        with self._connect() as con:
            con.execute("DELETE FROM habits WHERE id = ?", (habit_id,))

    def check_in_habit(self, habit_id: int):
        today = date.today().isoformat()
        with self._connect() as con:
            row = con.execute(
                "SELECT checkins FROM habits WHERE id = ?", (habit_id,)
            ).fetchone()
            if row is None:
                return
            checkins: list[str] = json.loads(row[0])
            if today not in checkins:
                checkins.append(today)
                con.execute(
                    "UPDATE habits SET checkins = ? WHERE id = ?",
                    (json.dumps(checkins), habit_id),
                )

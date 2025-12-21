from datetime import datetime
import sqlite3
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


DB_PATH = "vacancies.db"

app = FastAPI()


class VacancyInput(BaseModel):
    name: str
    salary: str
    area_name: str


def get_db_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def fetch_one(query: str, params: tuple = ()) -> sqlite3.Row | None:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchone()


def execute(query: str, params: tuple = ()) -> None:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()


@app.get("/vacancies/{vacancy_id}")
def get_vacancy(vacancy_id: int):
    vacancy = fetch_one(
        "SELECT * FROM vacancies WHERE id = ?",
        (vacancy_id,),
    )

    if not vacancy:
        return {"error": "vacancy not found"}

    return dict(vacancy)


@app.post("/vacancies")
def create_vacancy(vacancy: VacancyInput):
    row = fetch_one("SELECT MAX(id) AS max_id FROM vacancies")
    new_id = (row["max_id"] or 0) + 1

    execute(
        """
        INSERT INTO vacancies (id, name, salary, area_name, published_at)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            new_id,
            vacancy.name,
            vacancy.salary,
            vacancy.area_name,
            datetime.now().isoformat(),
        ),
    )

    return {"message": "vacancy posted successfully"}


@app.delete("/vacancies/{vacancy_id}")
def delete_vacancy(vacancy_id: int):
    vacancy = fetch_one(
        "SELECT id FROM vacancies WHERE id = ?",
        (vacancy_id,),
    )

    if not vacancy:
        return {"error": "vacancy not found"}

    execute(
        "DELETE FROM vacancies WHERE id = ?",
        (vacancy_id,),
    )

    return {"message": "vacancy deleted successfully"}

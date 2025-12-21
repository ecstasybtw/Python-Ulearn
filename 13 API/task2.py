import sqlite3
import pandas as pd


def load_currency(path: str) -> pd.DataFrame:
    return pd.read_csv(path, index_col="date")


def load_vacancies(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


def calc_salary(row: pd.Series) -> float | None:
    if pd.isna(row["salary_to"]):
        return row["salary_from"]
    if pd.isna(row["salary_from"]):
        return row["salary_to"]
    return (row["salary_from"] + row["salary_to"]) / 2


def convert_salary(row: pd.Series, rates: pd.DataFrame) -> float | None:
    if row["salary_currency"] == "RUR":
        return row["salary"]
    if pd.isna(row["salary_currency"]):
        return None

    date_key = row["date"]
    cur = row["salary_currency"]
    if date_key in rates.index and cur in rates.columns:
        return row["salary"] * rates.at[date_key, cur]

    return None


def prepare(df: pd.DataFrame, rates: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["id"] = df.index + 1
    df["date"] = pd.to_datetime(df["published_at"], errors="coerce", utc=True).dt.strftime("%Y-%m")
    df["salary"] = df.apply(calc_salary, axis=1)
    df["salary"] = df.apply(lambda row: convert_salary(row, rates), axis=1)
    return df


def save_to_sqlite(df: pd.DataFrame, db_path: str, table: str = "vacancies") -> None:
    with sqlite3.connect(db_path) as connection:
        (
            df[["id", "name", "salary", "area_name", "published_at"]]
            .set_index("id")
            .to_sql(table, connection)
        )


def main() -> None:
    rates = load_currency("valutes.csv")
    df = load_vacancies("vacancies_dif_currencies.csv")
    df = prepare(df, rates)
    save_to_sqlite(df, "student_works/vacancies.db")


if __name__ == "__main__":
    main()

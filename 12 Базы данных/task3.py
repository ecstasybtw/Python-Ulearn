import pandas as pd
import sqlite3

database_name = input()
table_name = input()
vac_name = input()

with sqlite3.connect(database_name) as conn:

    df_years_salary = pd.read_sql(f"""
        SELECT
            strftime('%Y', published_at) AS "Год",
            ROUND(AVG(salary), 2) AS "Средняя з/п"
        FROM {table_name}
        WHERE salary IS NOT NULL
        GROUP BY "Год"
        ORDER BY "Год"
    """, conn)

    df_years_count = pd.read_sql(f"""
        SELECT
            strftime('%Y', published_at) AS "Год",
            COUNT(*) AS "Количество вакансий"
        FROM {table_name}
        WHERE salary IS NOT NULL
        GROUP BY "Год"
        ORDER BY "Год"
    """, conn)

    df_years_salary_vac = pd.read_sql(f"""
        SELECT
            strftime('%Y', published_at) AS "Год",
            ROUND(AVG(salary), 2) AS "Средняя з/п - {vac_name}"
        FROM {table_name}
        WHERE salary IS NOT NULL
          AND name LIKE '%' || ? || '%'
        GROUP BY "Год"
        ORDER BY "Год"
    """, conn, params=(vac_name,))

    df_years_count_vac = pd.read_sql(f"""
        SELECT
            strftime('%Y', published_at) AS "Год",
            COUNT(*) AS "Количество вакансий - {vac_name}"
        FROM {table_name}
        WHERE salary IS NOT NULL
          AND name LIKE '%' || ? || '%'
        GROUP BY "Год"
        ORDER BY "Год"
    """, conn, params=(vac_name,))

    df_area_salary = pd.read_sql(f"""
		SELECT area_name AS "Город",
			   ROUND(AVG(salary), 2) AS "Уровень зарплат по городам"
		FROM {table_name}
		GROUP BY area_name
		HAVING COUNT(*) * 1.0 / (SELECT COUNT(*) FROM {table_name}) > 0.008
		ORDER BY "Уровень зарплат по городам" DESC
		LIMIT 10
	""", conn)

    df_area_count = pd.read_sql(f"""
		SELECT area_name AS "Город",
			   COUNT(*) * 1.0 / (SELECT COUNT(*) FROM {table_name}) AS "Доля вакансий"
		FROM {table_name}
		GROUP BY area_name
		HAVING COUNT(*) * 1.0 / (SELECT COUNT(*) FROM {table_name}) > 0.008
		ORDER BY "Доля вакансий" DESC
		LIMIT 10
	""", conn)

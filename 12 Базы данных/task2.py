import pandas as pd
import sqlite3
import re


database_name = input()
csv_file = input()
table_name = input()
currency_table = input()


def extact_ym(row: pd.Series):
    pattern = re.compile(r'\d{4}-\d{2}')
    return ''.join(pattern.findall(row['published_at']))


def get_ym_from_df(df: pd.DataFrame):
    df['date'] = df.apply(extact_ym, axis=1).astype(str)

    return df


def get_avg_salary(row: pd.Series):
    salary_from = row['salary_from']
    salary_to = row['salary_to']

    if pd.isna(salary_from) and pd.isna(salary_to):
        return pd.NA
    elif pd.isna(salary_from):
        return salary_to
    elif pd.isna(salary_to):
        return salary_from

    return (salary_from + salary_to) / 2


def convert_currency(df: pd.DataFrame, db_name: str, table_name: str):
    df = get_ym_from_df(df)

    with sqlite3.connect(db_name) as conn:
        currency_df = pd.read_sql(f"SELECT * FROM {table_name}", conn)

        currency_df_long = currency_df.melt(
            id_vars='date',
            var_name='salary_currency',
            value_name='rate'
        )

        working_on = df.merge(
            currency_df_long,
            how='left',
            left_on=['date', 'salary_currency'],
            right_on=['date', 'salary_currency']
        )

        mask_rur = working_on['salary_currency'] == 'RUR'
        working_on.loc[mask_rur, 'rate'] = 1

        working_on['salary_from'] = working_on['salary_from'] * working_on['rate']
        working_on['salary_to'] = working_on['salary_to'] * working_on['rate']

        working_on['average_salary'] = working_on.apply(get_avg_salary, axis=1)
        working_on['average_salary'] = working_on['average_salary'].apply(
            lambda x: int(x) if pd.notna(x) else pd.NA
        )


    return working_on


def convert_to_db(df: pd.DataFrame, db_name: str, table_name: str):
    result_df = df[[
        'name',
        'average_salary',
        'area_name',
        'published_at'
    ]].rename(columns={'average_salary': 'salary'})

    result_df['published_at'] = (
        pd.to_datetime(result_df['published_at'])
        .dt.strftime('%Y-%m-%dT%H:%M:%S%z')
        .str.replace(r'(\+|\-)(\d{2})(\d{2})$', r'\1\2:\3', regex=True)
    )

    with sqlite3.connect(db_name) as conn:
        result_df.to_sql(
            table_name,
            conn,
            if_exists='replace',
            index=False
        )


def main():
    df = pd.read_csv(csv_file)
    working_on = convert_currency(df, database_name, currency_table)
    convert_to_db(working_on, database_name, table_name)


if __name__ == '__main__':
    main()

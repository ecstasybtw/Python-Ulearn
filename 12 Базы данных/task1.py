import pandas as pd
import sqlite3


database_name = input()
csv_file = input()
table_name = input()


def main():

    df = pd.read_csv(csv_file)

    with sqlite3.connect(database_name) as conn:
        df.to_sql(
            table_name,
            conn,
            if_exists='replace',
            index = False
        )


if __name__ == '__main__':
    main()

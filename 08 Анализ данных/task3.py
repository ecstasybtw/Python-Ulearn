import pandas as pd


def get_avg_sal(row):
    if pd.isna(row['salary_from']):
        return row['salary_to']
    elif pd.isna(row['salary_to']):
        return row['salary_from']
    return (row['salary_from'] + row['salary_to']) / 2


def extract_cities(df: pd.DataFrame):

    mask = df["salary_currency"] == "RUR"
    subset = df.loc[mask].copy()

    subset['average_salary'] = subset.apply(get_avg_sal, axis=1)
    subset = (
        subset
        .groupby('area_name')['average_salary']
        .mean()
        .round()
        .astype(int)
        .sort_values(ascending=False)
        )

    dct = subset.to_dict()
    sorted_ = sorted(
        dct.items(),
        key=lambda item:[-item[1], item[0]],
    )

    sorted_dct = {}
    for t in sorted_:
        sorted_dct[t[0]] = t[1]

    print(sorted_dct)


def main():
    vacancies = pd.read_csv('vacancies_small.csv')
    extract_cities(vacancies)


if __name__ == '__main__':
    main()

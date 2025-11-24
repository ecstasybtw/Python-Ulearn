import pandas as pd


def get_years(subset: pd.DataFrame):
    years = (pd.to_datetime(subset['published_at'])
        .dt
        .year
        )

    return years


def get_avg_sal(row):
    if pd.isna(row['salary_from']):
        return row['salary_to']
    elif pd.isna(row['salary_to']):
        return row['salary_from']
    return (row['salary_to'] + row['salary_from']) / 2


def get_dict(ls: list):
    dct = {}
    for t in ls:
        dct[t[0]] = t[1]

    return dct

def get_subset(df: pd.DataFrame, profession: str = None):
    mask = (df['salary_currency'] == 'RUR') & (
            pd.to_datetime(df['published_at'])
            .dt
            .year >= 2019
        )

    subset = df.loc[mask].copy()

    if profession is not None:
        subset = subset[subset['name'].str.contains(profession, case=False, na=False)]

    subset['average_salary'] = subset.apply(get_avg_sal, axis=1).round().astype(int)

    return subset


def get_salary_by_years(df: pd.DataFrame, profession: str):
    subset = get_subset(df, profession)

    years = get_years(subset)
    ys = (
        subset
        .groupby(years)
        ['average_salary']
        .mean()
        .round()
        .astype(int)
        .sort_values(ascending=False)
        )
    dct = ys.to_dict()
    sorted_ = sorted(
        dct.items(),
        key = lambda item: item[0]
    )

    sorted_dct = get_dict(sorted_)

    print("Динамика уровня зарплат по годам для выбранной профессии:", sorted_dct)


def get_vcount_by_years(df: pd.DataFrame, profession: str):
    subset = get_subset(df, profession)

    years = get_years(subset)
    yv = (
        subset
        .groupby(years)
        ['name']
        .count()
        .sort_values(ascending=False)
        )

    dct = yv.to_dict()
    sorted_ = sorted(
        dct.items(),
        key = lambda item: item[0]
    )

    sorted_dct = get_dict(sorted_)

    print("Динамика количества вакансий по годам для выбранной профессии:", sorted_dct)


def get_all_salary_by_years(df: pd.DataFrame):
    subset = get_subset(df)
    years = get_years(subset)
    alls = (
        subset
        .groupby(years)
        ['average_salary']
        .mean()
        .astype(int)
        .sort_values(ascending=False)
        )
    dct = alls.to_dict()
    sorted_ = sorted(
        dct.items(),
        key = lambda item: item[0]
    )

    sorted_dct = get_dict(sorted_)

    print("Динамика уровня зарплат по годам:", sorted_dct)


def get_avcount_by_years(df: pd.DataFrame):
    subset = get_subset(df)

    years = get_years(subset)
    yv = (
        subset
        .groupby(years)
        ['name']
        .count()
        .sort_values(ascending=False)
        )

    dct = yv.to_dict()
    sorted_ = sorted(
        dct.items(),
        key = lambda item: item[0]
    )

    sorted_dct = get_dict(sorted_)

    print("Динамика количества вакансий по годам:", sorted_dct)


def sal_level_for_prof(df: pd.DataFrame, profession: str):
    subset = get_subset(df, profession)

    cs = (
        subset
        .groupby('area_name')
        ['average_salary']
        .mean()
        .astype(int)
        .sort_values(ascending=True)
    )

    dct = cs.to_dict()
    sorted_ = sorted(
        dct.items(),
        key = lambda item: [-item[1], item[0]]
    )
    sorted_dct = get_dict(sorted_)
    print('Уровень зарплат по городам для выбранной профессии (в порядке убывания):', sorted_dct)


def get_amout_vac_prof(df: pd.DataFrame, profession: str):
    subset_with_p = get_subset(df, profession)

    total = len(subset_with_p)

    grouped = (
        subset_with_p
        .groupby('area_name')
        ['name']
        .count()
    )

    dct = {}
    for city, count in grouped.items():
        dct[city] = round(count / total, 4)

    sorted_ = sorted(
        dct.items(),
        key=lambda item: (-item[1], item[0])
    )

    top10 = sorted_[:10]

    sorted_dct = get_dict(top10)

    print("Доля вакансий по городам для выбранной профессии (в порядке убывания):", sorted_dct)


def main():
    vacancies = pd.read_csv('vacancies_for_learn_demo.csv')
    profession = input()
    get_all_salary_by_years(vacancies)
    get_avcount_by_years(vacancies)
    get_salary_by_years(vacancies, profession)
    get_vcount_by_years(vacancies, profession)
    sal_level_for_prof(vacancies, profession)
    get_amout_vac_prof(vacancies, profession)

if __name__ == '__main__':
    main()

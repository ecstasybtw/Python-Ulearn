import pandas as pd
import numpy as np


def prepare_dataset(path_to_csv: str):
    df = pd.read_csv(path_to_csv)

    df['pub_year'] = pd.to_datetime(df['published_at'], errors='coerce').dt.year
    df['unit'] = 0

    df['avg_sal'] = df[['salary_from', 'salary_to']].mean(axis=1)
    df['avg_sal'] = df['avg_sal'].apply(np.floor).astype(int)

    upper_year = df['pub_year'].max()
    mask = (df['salary_currency'] == 'RUR') & (df['pub_year'] >= upper_year - 4)

    return df.loc[mask].copy()


def yearly_salary_stats(df_years: pd.DataFrame):
    res = (
        df_years
        .groupby('pub_year')['avg_sal']
        .mean()
        .apply(np.floor)
        .astype(int)
    )
    return res.iloc[-5:].to_dict()


def yearly_count_stats(df_years: pd.DataFrame):
    freq = df_years.groupby('pub_year')['unit'].count()
    return freq.iloc[-5:].to_dict()


def profession_salary_by_year(df_prof: pd.DataFrame, yr_range):
    data = (
        df_prof
        .groupby('pub_year')['avg_sal']
        .mean()
        .apply(np.floor)
        .astype(int)
        .reindex(yr_range, fill_value=0)
    )
    return data.to_dict()


def profession_count_by_year(df_prof: pd.DataFrame, yr_range):
    data = (
        df_prof
        .groupby('pub_year')['unit']
        .count()
        .reindex(yr_range, fill_value=0)
    )
    return data.to_dict()


def top_cities_salary(df_prof: pd.DataFrame, cnt_total: int):
    block = df_prof.groupby('area_name').agg(
        mean_val=('avg_sal', 'mean'),
        qty=('unit', 'count')
    )

    block['mean_val'] = block['mean_val'].apply(np.floor).astype(int)
    block['share'] = block['qty'] / cnt_total

    block = block.query('share >= 0.01')
    ordered = block.sort_values(['mean_val', 'area_name'], ascending=[False, True])

    return ordered.iloc[:10]['mean_val'].to_dict()


def top_cities_share(df_prof: pd.DataFrame, cnt_total: int):
    block = df_prof.groupby('area_name').agg(qty=('unit', 'count'))
    block['share'] = block['qty'] / cnt_total

    block = block.query('share >= 0.01').round({'share': 4})
    ordered = block.sort_values(['share', 'area_name'], ascending=[False, True])

    return ordered.iloc[:10]['share'].to_dict()


def run_analysis():
    file_src = 'vacancies_for_learn_demo.csv'
    prof = input()

    df = prepare_dataset(file_src)

    last_year = df['pub_year'].max()
    years = pd.Series(range(last_year - 4, last_year + 1))

    general_salary = yearly_salary_stats(df)
    general_count = yearly_count_stats(df)

    df_prof = df[df['name'].str.contains(prof, na=False)]

    prof_salary = profession_salary_by_year(df_prof, years)
    prof_count = profession_count_by_year(df_prof, years)

    prof_total = len(df_prof)

    cities_salary = top_cities_salary(df_prof, prof_total)
    cities_share = top_cities_share(df_prof, prof_total)

    print(f'Динамика уровня зарплат по годам: {general_salary}')
    print(f'Динамика количества вакансий по годам: {general_count}')
    print(f'Динамика уровня зарплат по годам для выбранной профессии: {prof_salary}')
    print(f'Динамика количества вакансий по годам для выбранной профессии: {prof_count}')
    print(f'Уровень зарплат по городам для выбранной профессии (в порядке убывания): {cities_salary}')
    print(f'Доля вакансий по городам для выбранной профессии (в порядке убывания): {cities_share}')


if __name__ == '__main__':
    run_analysis()

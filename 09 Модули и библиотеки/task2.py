import openpyxl as op
import pandas as pd
import matplotlib.pyplot as plt


def get_years(df: pd.DataFrame):
    return pd.to_datetime(df['created_at']).dt.year


def get_profession_mask(df: pd.DataFrame, profession: str):
    mask = df['name'].str.contains(profession, case=False, na=False)
    subset = df.loc[mask].copy()
    return subset


def get_average_salary(row):
    if pd.isna(row['salary_from']):
        return row['salary_to']
    if pd.isna(row['salary_to']):
        return row['salary_from']
    return (row['salary_from'] + row['salary_to']) / 2


def read_csv(filename):
    df = pd.read_csv(
        filename,
        header=None,
        names=['name', 'salary_from', 'salary_to', 'salary_currency', 'area_name', 'created_at']
    )
    df['created_at'] = pd.to_datetime(df['created_at'], utc=True)
    df['average_salary'] = df.apply(get_average_salary, axis=1)
    return df


def get_city_shares(df: pd.DataFrame):
    total = len(df)
    city_counts = df['area_name'].value_counts()
    return (city_counts / total) * 100


def aggregate_by_year(df: pd.DataFrame, column: str, agg_func: str, profession: str = None):
    if profession:
        df = get_profession_mask(df, profession)

    years = get_years(df)

    subset = (
        df
        .groupby(years)[column]
        .agg(agg_func)
    )

    if agg_func == 'mean':
        subset = subset.round().astype(int)
    else:
        subset = subset.astype(int)

    dct = subset.to_dict()
    sorted_items = sorted(dct.items(), key=lambda item: item[0])
    return dict(sorted_items)


def get_sal_by_year(df: pd.DataFrame):
    return aggregate_by_year(df, 'average_salary', 'mean')


def get_vaccount_by_year(df: pd.DataFrame):
    return aggregate_by_year(df, 'name', 'count')


def get_profvaccount_by_year(df: pd.DataFrame, profession: str):
    return aggregate_by_year(df, 'name', 'count', profession)


def get_profsal_by_year(df: pd.DataFrame, profession: str):
    return aggregate_by_year(df, 'average_salary', 'mean', profession)


def get_sal_by_city(df: pd.DataFrame):
    city_shares = get_city_shares(df)
    valid_cities = city_shares[city_shares > 1].index

    subset = df[df['area_name'].isin(valid_cities)]

    subset = (
        subset
        .groupby('area_name')['average_salary']
        .mean()
        .round()
        .astype(int)
    )

    dct = subset.to_dict()

    sorted_items = sorted(
        dct.items(),
        key=lambda item: (-item[1], item[0])
    )

    return dict(sorted_items[:10])


def get_share_by_city(df: pd.DataFrame):
    city_shares = get_city_shares(df)
    city_shares = city_shares[city_shares > 1].round(2)

    sorted_items = sorted(
        city_shares.items(),
        key=lambda item: (-item[1], item[0])
    )

    top_10 = sorted_items[:10]
    return dict(top_10)


def wrap_city_name(city):
    parts = city.replace('-', ' ').split()
    return "\n".join(parts)


def create_plot():
    df = read_csv('vacancies.csv')

    profession = 'программист'

    salary_by_year = get_sal_by_year(df)
    prof_salary_by_year = get_profsal_by_year(df, profession)

    vacancies_by_year = get_vaccount_by_year(df)
    prof_vacancies_by_year = get_profvaccount_by_year(df, profession)

    years = list(salary_by_year.keys())
    x = list(range(len(years)))
    width = 0.4

    salary_by_city = get_sal_by_city(df)
    share_by_city = get_share_by_city(df)

    fig, sub = plt.subplots(2, 2)
    ax1, ax2, ax3, ax4 = sub.flatten()

    ax1.bar(
        [i - width / 2 for i in x],
        [salary_by_year[y] for y in years],
        width,
        label="средняя з/п"
    )
    ax1.bar(
        [i + width / 2 for i in x],
        [prof_salary_by_year.get(y, 0) for y in years],
        width,
        label=f"з/п {profession}"
    )
    ax1.set_xticks(x)
    ax1.set_xticklabels(years, rotation=90, fontsize=8)
    ax1.set_yticklabels(ax1.get_yticks(), fontsize=8)
    ax1.set_title("Уровень зарплат по годам", fontsize=8)
    ax1.grid(True, axis='y')
    ax1.legend(fontsize=8)

    ax2.bar(
        [i - width / 2 for i in x],
        [vacancies_by_year[y] for y in years],
        width,
        label="Количество вакансий"
    )
    ax2.bar(
        [i + width / 2 for i in x],
        [prof_vacancies_by_year.get(y, 0) for y in years],
        width,
        label=f"Количество вакансий {profession}"
    )
    ax2.set_xticks(x)
    ax2.set_xticklabels(years, rotation=90, fontsize=8)
    ax2.set_yticklabels(ax2.get_yticks(), fontsize=8)
    ax2.set_title("Количество вакансий по годам", fontsize=8)
    ax2.grid(True, axis='y')
    ax2.legend(fontsize=8)


    cities = list(salary_by_city.keys())
    salaries = list(salary_by_city.values())

    y_pos = range(len(cities))

    ax3.barh(y_pos, salaries)
    ax3.set_yticks(y_pos)
    ax3.set_yticklabels(
        [wrap_city_name(c) for c in cities],
        fontsize=6,
        horizontalalignment='right',
        verticalalignment='center'
    )
    ax3.set_xticklabels(ax3.get_xticks(), fontsize=8)
    ax3.set_title("Уровень зарплат по городам", fontsize=8)
    ax3.grid(True, axis='x')
    ax3.invert_yaxis()

    labels = list(share_by_city.keys())
    sizes = list(share_by_city.values())
    other = max(0.0, 100.0 - sum(sizes))
    if other > 0.1:
        labels.append("Другие")
        sizes.append(other)

    ax4.pie(
        sizes,
        labels=labels,
        textprops={'fontsize': 6},
        startangle=140
    )
    ax4.set_title("Доля вакансий по городам", fontsize=8)

    plt.tight_layout()
    # return sub

    plt.show()


if __name__ == '__main__':
    create_plot()

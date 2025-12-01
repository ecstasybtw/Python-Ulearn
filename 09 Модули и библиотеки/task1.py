import openpyxl as op
from openpyxl.styles import Border, Side, Font
import pandas as pd


def get_years(df: pd.DataFrame):
    return pd.to_datetime(df['created_at']).dt.year


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


def aggregate_by_year(df: pd.DataFrame, column: str, agg_func: str):
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


def create_border():
    return Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin')
    )


def setup_years_sheet(sheet):
    sheet.title = 'Статистика по годам'
    sheet['A1'] = 'Год'
    sheet['B1'] = 'Средняя зарплата'
    sheet['C1'] = 'Количество вакансий'

    sheet['A1'].font = Font(bold=True)
    sheet['B1'].font = Font(bold=True)
    sheet['C1'].font = Font(bold=True)

    sheet.column_dimensions['A'].width = 6
    sheet.column_dimensions['B'].width = 20
    sheet.column_dimensions['C'].width = 20


def setup_cities_sheet(sheet):
    sheet.title = 'Статистика по городам'
    sheet['A1'] = 'Город'
    sheet['B1'] = 'Уровень зарплат'
    sheet['D1'] = 'Город'
    sheet['E1'] = 'Доля вакансий, %'

    sheet['A1'].font = Font(bold=True)
    sheet['B1'].font = Font(bold=True)
    sheet['D1'].font = Font(bold=True)
    sheet['E1'].font = Font(bold=True)

    sheet.column_dimensions['A'].width = 20
    sheet.column_dimensions['B'].width = 20
    sheet.column_dimensions['C'].width = 2
    sheet.column_dimensions['D'].width = 20
    sheet.column_dimensions['E'].width = 20


def fill_years_sheet(sheet, salary_by_years, vacancies_by_years, border):
    for index, (year, salary) in enumerate(salary_by_years.items()):
        row = index + 2
        sheet[f'A{row}'] = year
        sheet[f'B{row}'] = salary

    for index, (year, count) in enumerate(vacancies_by_years.items()):
        row = index + 2
        sheet[f'C{row}'] = count

    for row in sheet['A1:C17']:
        for cell in row:
            cell.border = border


def fill_cities_sheet(sheet, salary_by_cities, share_by_city, border):
    for index, (city, salary) in enumerate(salary_by_cities.items()):
        row = index + 2
        sheet[f'A{row}'] = city
        sheet[f'B{row}'] = salary

    for index, (city, share) in enumerate(share_by_city.items()):
        row = index + 2
        sheet[f'D{row}'] = city
        sheet[f'E{row}'] = share

    for row in sheet['A1:B11']:
        for cell in row:
            cell.border = border

    for row in sheet['D1:E11']:
        for cell in row:
            cell.border = border


def create_report(df):
    wb = op.Workbook()

    years_sheet = wb.active
    cities_sheet = wb.create_sheet(title='Статистика по городам', index=1)

    setup_years_sheet(years_sheet)
    setup_cities_sheet(cities_sheet)

    salary_by_years = get_sal_by_year(df)
    vacancies_by_years = get_vaccount_by_year(df)

    salary_by_cities = get_sal_by_city(df)
    share_by_city = get_share_by_city(df)

    border = create_border()

    fill_years_sheet(years_sheet, salary_by_years, vacancies_by_years, border)
    fill_cities_sheet(cities_sheet, salary_by_cities, share_by_city, border)

    wb.save('student_works/report.xlsx')


def main():
    df = read_csv('vacancies.csv')
    create_report(df)


if __name__ == '__main__':
    main()

import pandas as pd

def filter_csv(df, column, sort_by, keyword, sort_type):
    ascending = True if sort_type == 'asc' else False

    filtered_df = df[df[column].str.contains(keyword, case=False, na=False)].copy()

    filtered_df = filtered_df.sort_index()

    filtered_df = filtered_df.sort_values(
        by=sort_by,
        ascending=ascending,
        kind='mergesort'
    )

    return filtered_df['name'].tolist()


def main():
    df = pd.read_csv('vacancies_small.csv')
    column = input()
    keyword = input()
    sort_by = input()
    sort_type = input()
    filtered = filter_csv(df, column, sort_by, keyword, sort_type)
    print(filtered)


if __name__ == "__main__":
    vacancies = pd.read_csv('vacancies_small.csv')
    main()

import pandas as pd
from collections import Counter


def extract_top_skills(csv_path: str, profession: str, order: str = "asc", top_n: int = 5):
    df = pd.read_csv(csv_path)
    mask = df['name'].str.contains(profession, case=False, na=False)
    subset = df.loc[mask].copy()

    subset['row_id'] = subset.index

    def to_list(val):
        if isinstance(val, str):
            return val.split('\n')
        return []
    subset['key_skills'] = subset['key_skills'].apply(to_list)

    freq = []
    first_seen = {}

    for row_idx, skill_list in subset['key_skills'].items():
        for s in skill_list:
            freq.append(s)
            if s not in first_seen:
                first_seen[s] = row_idx

    counter = Counter(freq)
    reverse_flag = (order == "asc")
    sorted_pairs = sorted(
        counter.items(),
        key=lambda item: (item[1], first_seen[item[0]]),
        reverse=reverse_flag
    )

    return sorted_pairs[:top_n]


def main():
    profession = input()
    order = input()
    result = extract_top_skills('vacancies_small.csv', profession, order, 5)
    print(result)


if __name__ == "__main__":
    main()






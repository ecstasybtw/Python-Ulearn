from concurrent.futures import ProcessPoolExecutor
import re


def parse_string_to_list(string: str) -> list[list[int]]:

    pattern = re.compile(r'\[(\d+(?:\s+\d+)*)\]')
    ls = pattern.findall(string)

    parsed = []

    for group in ls:
        parsed.append([int(num) for num in group.split()])

    return parsed


def main():
    array_2d = input()

    parsed = parse_string_to_list(array_2d)

    with ProcessPoolExecutor() as executor:

        results_iter = executor.map(worker_function, parsed)
        results = list(results_iter)

    result = 0

    for res in results:
        result += res

    print(result)


if __name__ == "__main__":
    main()

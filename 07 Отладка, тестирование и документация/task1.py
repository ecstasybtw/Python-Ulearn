import cProfile
import pstats
import time
import random

def load_files():
    data = [random.random() for _ in range(10**6)]
    time.sleep(0.1)
    sum(data)

def read_database():
    result = [i**2 for i in range(10**6)]
    time.sleep(0.15)
    sum(result)

def get_id():
    ids = [str(i) for i in range(10**5)]
    time.sleep(0.05)
    "_".join(ids)

def get_user_data():
    users = [{"id": i, "name": f"user{i}"} for i in range(10**5)]
    time.sleep(0.1)
    [u["name"].upper() for u in users]

def generate_words():
    words = ["word" + str(i) for i in range(5 * 10**5)]
    time.sleep(0.08)
    "".join(words)


TASK_FUNCTIONS_ORDER = [load_files, read_database, get_id, get_user_data, generate_words]

def profile_functions(order):
    with cProfile.Profile() as profile:
        for function in order:
            function()
    stats = pstats.Stats(profile)
    stats = stats.sort_stats('cumulative')
    return stats

def return_stats(stats):
    profilings = []
    total_time = sum(data[3] for data in stats.stats.values())
    for function in TASK_FUNCTIONS_ORDER:
        name = function.__name__
        for (file, line, fname), data in stats.stats.items():
            if fname == name:
                percent = (data[3] / total_time) * 100
                profilings.append(f"{data[3]:.4f}: {int(round(percent))}%")
                break
    return profilings

def main():
    stats = profile_functions(TASK_FUNCTIONS_ORDER)
    profilings = return_stats(stats)
    print('\n'.join(profilings))

if __name__ == '__main__':
    main()

import os


def save_best_time(best_time: float):
    with open("best_time.txt", "w") as file:
        file.write(str(best_time))


def read_best_time():
    if os.path.exists("best_time.txt"):
        with open("best_time.txt", "r") as file:
            return file.read().strip()
    return "0"

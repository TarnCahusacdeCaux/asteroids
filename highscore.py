import os


def save_highscore(highscore: int):
    with open("highscore.txt", "w") as file:
        file.write(str(highscore))


def read_highscore():
    if os.path.exists("highscore.txt"):
        with open("highscore.txt", "r") as file:
            return file.read().strip()
    return "0"

import pandas as pd
import os


def load_channels(csv_url):
    df = pd.read_csv(csv_url)

    # 假设列名：channel / count
    return df.to_dict("records")


def load_sent():
    if not os.path.exists("sent.txt"):
        return set()
    return set(open("sent.txt").read().splitlines())


def save_sent(url):
    with open("sent.txt", "a") as f:
        f.write(url + "\n")

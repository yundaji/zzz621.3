import os
import requests
import pandas as pd
from io import StringIO


# =========================
# 📌 读取频道
# =========================
def load_channels(csv_url):

    r = requests.get(csv_url, timeout=20)
    r.raise_for_status()

    df = pd.read_csv(StringIO(r.text))

    df.columns = [c.strip().lower() for c in df.columns]

    if "channel" not in df.columns:
        raise ValueError("CSV必须包含 channel 列")

    if "count" not in df.columns:
        df["count"] = 1

    df = df.dropna(subset=["channel"])

    channels = []

    for _, row in df.iterrows():
        ch = str(row["channel"]).strip()

        if ch:
            channels.append({
                "channel": ch,
                "count": int(row["count"]) if str(row["count"]).isdigit() else 1
            })

    return channels


# =========================
# 📌 已发送记录
# =========================
def load_sent():
    if not os.path.exists("sent.txt"):
        return set()

    with open("sent.txt", "r", encoding="utf-8") as f:
        return set(f.read().splitlines())


# =========================
# 🚨 是否已发送
# =========================
def is_sent(url):
    if not os.path.exists("sent.txt"):
        return False

    with open("sent.txt", "r", encoding="utf-8") as f:
        return url.strip() in f.read().splitlines()


# =========================
# 💾 保存记录
# =========================
def save_sent(url):
    with open("sent.txt", "a", encoding="utf-8") as f:
        f.write(url.strip() + "\n")

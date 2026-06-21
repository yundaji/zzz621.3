import os


# =========================
# 📌 已发送记录
# =========================
def load_sent():
    if not os.path.exists("sent.txt"):
        return set()

    with open("sent.txt", "r", encoding="utf-8") as f:
        return set(f.read().splitlines())


# =========================
# 🚨 实时判断是否已发送（关键）
# =========================
def is_sent(url):
    if not os.path.exists("sent.txt"):
        return False

    with open("sent.txt", "r", encoding="utf-8") as f:
        return url.strip() in f.read().splitlines()


# =========================
# 💾 保存已发送
# =========================
def save_sent(url):
    with open("sent.txt", "a", encoding="utf-8") as f:
        f.write(url.strip() + "\n")

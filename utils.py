import os
import requests
import pandas as pd
from io import StringIO


# =========================
# 📌 读取频道（稳定版）
# =========================
def load_channels(csv_url):
    try:
        # 🔥 用 requests 拉 CSV（比 pandas 直接读 URL 更稳定）
        r = requests.get(csv_url, timeout=20)
        r.raise_for_status()

        content = r.text.strip()

        # 读取 CSV
        df = pd.read_csv(StringIO(content))

        # 🔥 统一列名（避免 Channel / channel 不一致）
        df.columns = [c.strip().lower() for c in df.columns]

        # 必须字段检查
        if "channel" not in df.columns:
            raise ValueError("CSV 必须包含 channel 列")

        if "count" not in df.columns:
            df["count"] = 1

        # 删除空数据
        df = df.dropna(subset=["channel"])

        channels = []

        for _, row in df.iterrows():
            channel = str(row["channel"]).strip()

            if not channel:
                continue

            channels.append({
                "channel": channel,
                "count": int(row["count"]) if str(row["count"]).isdigit() else 1
            })

        print(f"✅ 读取频道成功：{len(channels)} 个")

        return channels

    except Exception as e:
        print("❌ 读取CSV失败：", e)
        return []


# =========================
# 📌 已发送记录
# =========================
def load_sent():
    if not os.path.exists("sent.txt"):
        return set()

    with open("sent.txt", "r", encoding="utf-8") as f:
        return set(f.read().splitlines())


# =========================
# 📌 保存已发送
# =========================
def save_sent(url):
    with open("sent.txt", "a", encoding="utf-8") as f:
        f.write(url + "\n")

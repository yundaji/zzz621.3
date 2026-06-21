import asyncio
from fetch import get_article
from tg import init, send_post
from utils import load_channels, load_sent, save_sent
from config import BOT_TOKEN, CSV_URL


# =========================
# 🧠 文章池（唯一来源）
# =========================
def get_pool():
    return [
        "https://www.mhwmm.com/miandianxinwen/81512.html",
        "https://www.mhwmm.com/miandianxinwen/81511.html",
        "https://www.mhwmm.com/miandianxinwen/81510.html",
        "https://www.mhwmm.com/miandianxinwen/81509.html",
        "https://www.mhwmm.com/miandianxinwen/81508.html",
    ]


async def main():

    init(BOT_TOKEN)

    channels = load_channels(CSV_URL)
    sent = load_sent()

    pool = [u for u in get_pool() if u not in sent]

    if not pool:
        print("没有可用文章")
        return

    channel_index = 0

    # =========================
    # 🔥 核心：文章驱动分发
    # =========================
    for url in pool:

        article = get_article(url)

        # 👉 轮流选择频道
        channel = channels[channel_index % len(channels)]["channel"]

        await send_post(channel, article)

        print(f"已发送：{url} -> {channel}")

        # ✔ 全局去重锁定
        save_sent(url)

        channel_index += 1


if __name__ == "__main__":
    asyncio.run(main())

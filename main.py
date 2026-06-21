import asyncio
from fetch import get_article
from tg import init, send_post
from utils import load_channels, load_sent, save_sent
from config import BOT_TOKEN, CSV_URL


# 👉 自动文章池（建议后面改成列表页抓取）
URLS = [
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

    # ✅ 过滤已发送
    pool = [u for u in URLS if u not in sent]

    if not pool:
        print("没有可发送文章")
        return

    pool_index = 0

    # 🔥 核心：所有频道共享文章池
    for channel_cfg in channels:

        channel = channel_cfg["channel"]
        count = int(channel_cfg.get("count", 1))

        for _ in range(count):

            if pool_index >= len(pool):
                print("文章不够分配")
                return

            url = pool[pool_index]
            pool_index += 1

            article = get_article(url)

            await send_post(channel, article)

            print(f"发送成功：{channel} -> {url}")

            save_sent(url)


if __name__ == "__main__":
    asyncio.run(main())

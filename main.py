import asyncio
import random

from fetch import get_article, get_article_list
from tg import init, send_post
from utils import load_channels, load_sent, save_sent
from config import BOT_TOKEN, CSV_URL


async def main():

    init(BOT_TOKEN)

    # 频道配置
    channels = load_channels(CSV_URL)

    # 已发送去重池
    sent = set(load_sent())

    # 🧠 获取“文章池”（重点修复）
    urls = get_article_list()

    # ❗过滤已发送
    pool = [u for u in urls if u not in sent]

    if not pool:
        print("没有可发送的文章")
        return

    # 打乱顺序，避免重复模式
    random.shuffle(pool)

    # 🧠 记录每个频道分配的文章
    channel_cursor = {c["channel"]: [] for c in channels}

    idx = 0

    # 🔥 核心：给每个频道分配不同文章
    for c in channels:

        channel = c["channel"]
        count = int(c.get("count", 1))

        for _ in range(count):

            if idx >= len(pool):
                print("文章不够分配了")
                break

            url = pool[idx]
            idx += 1

            article = get_article(url)

            await send_post(channel, article)

            print(f"已发送 {channel} -> {url}")

            # 全局去重
            sent.add(url)
            save_sent(url)


if __name__ == "__main__":
    asyncio.run(main())

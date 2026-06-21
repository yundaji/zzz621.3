import asyncio
from fetch import get_article
from tg import init, send_post
from utils import load_channels, load_sent, save_sent
from config import BOT_TOKEN, CSV_URL, START_URL


async def main():

    init(BOT_TOKEN)

    channels = load_channels(CSV_URL)
    sent = load_sent()

    url = START_URL

    # 只示例1篇，你可以扩展抓列表页
    if url in sent:
        return

    article = get_article(url)

    index = 0

    for c in channels:

        channel = c["channel"]
        count = int(c.get("count", 1))

        for _ in range(count):

            await send_post(channel, article)

            print(f"已发送到 {channel}")

        index += 1

    save_sent(url)


if __name__ == "__main__":
    asyncio.run(main())

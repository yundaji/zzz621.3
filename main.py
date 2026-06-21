import asyncio
from fetch import get_article
from tg import init, send_post
from utils import load_channels, load_sent, save_sent
from config import BOT_TOKEN, CSV_URL


# =========================
# 🧠 文章池
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

    # =========================
    # 🚨 强制检查频道数量
    # =========================
    print(f"✅ 实际读取频道数量：{len(channels)}")

    if len(channels) == 0:
        print("❌ 没有读取到任何频道")
        return

    pool = [u for u in get_pool() if u not in sent]

    if not pool:
        print("没有可用文章")
        return

    # =========================
    # 🔥 核心优化：双循环防止只跑少数频道
    # =========================
    channel_index = 0
    channel_len = len(channels)

    for url in pool:

        article = get_article(url)

        # 👉 强制循环所有频道（关键修复）
        channel = channels[channel_index % channel_len]["channel"]

        await send_post(channel, article)

        print(f"已发送：{url} -> {channel}")

        save_sent(url)

        channel_index += 1

        # 🔥 防止 Telegram 限流（很重要）
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())

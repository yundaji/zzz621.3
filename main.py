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

    print(f"✅ 读取频道数量：{len(channels)}")

    if not channels:
        print("❌ 没有频道")
        return

    pool = [u for u in get_pool() if u not in sent]

    if not pool:
        print("没有可用文章")
        return

    channel_index = 0
    channel_len = len(channels)

    # =========================
    # 🔥 核心稳定分发逻辑
    # =========================
    for url in pool:

        article = get_article(url)

        channel = channels[channel_index % channel_len]["channel"]

        print(f"准备发送：{url} -> {channel}")

        try:
            await send_post(channel, article)
            print(f"✅ 已发送：{url} -> {channel}")

            save_sent(url)

        except Exception as e:
            print(f"❌ 发送失败：{channel} -> {e}")

            # ⚠️ 不影响整体继续
            channel_index += 1
            continue

        channel_index += 1

        # 🔥 防止 Telegram 限流（非常重要）
        await asyncio.sleep(1)


# =========================
# 🚀 正确入口
# =========================
if __name__ == "__main__":
    asyncio.run(main())

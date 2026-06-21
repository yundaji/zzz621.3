import asyncio
from fetch import get_article
from tg import init, send_post
from utils import load_channels, load_sent, save_sent
from config import BOT_TOKEN, CSV_URL


# =========================
# 🧠 全站文章池（动态）
# =========================
def get_pool():
    import requests
    from bs4 import BeautifulSoup
    from urllib.parse import urljoin

    url = "https://www.mhwmm.com/miandianxinwen.html"
    base = "https://www.mhwmm.com"

    headers = {"User-Agent": "Mozilla/5.0"}

    r = requests.get(url, headers=headers, timeout=15)
    r.encoding = "utf-8"

    soup = BeautifulSoup(r.text, "lxml")

    urls = []

    for a in soup.find_all("a"):
        href = a.get("href")

        if not href:
            continue

        if "miandianxinwen" not in href:
            continue

        full_url = urljoin(base, href)
        urls.append(full_url)

    # 去重
    urls = list(dict.fromkeys(urls))

    print(f"✅ 文章池数量：{len(urls)}")

    return urls


async def main():

    init(BOT_TOKEN)

    # =========================
    # 📌 读取频道
    # =========================
    channels = load_channels(CSV_URL)
    sent = load_sent()

    print(f"✅ 读取频道数量：{len(channels)}")

    if not channels:
        print("❌ 没有读取到频道")
        return

    # =========================
    # 📌 获取文章池
    # =========================
    pool = [u for u in get_pool() if u not in sent]

    if not pool:
        print("没有可用文章")
        return

    channel_index = 0
    channel_len = len(channels)

    # =========================
    # 🔥 核心分发逻辑
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

        channel_index += 1

        # 🔥 防止 Telegram 限流
        await asyncio.sleep(1)


# =========================
# 🚀 正确入口
# =========================
if name == "main":
    asyncio.run(main())

import asyncio
from fetch import get_article
from tg import init, send_post
from utils import load_channels, load_sent, save_sent, is_sent
from config import BOT_TOKEN, CSV_URL


# =========================
# 🧠 文章池（自动抓取）
# =========================
def get_pool():
    import requests
    from bs4 import BeautifulSoup
    from urllib.parse import urljoin

    url = "https://www.mhwmm.com/miandianxinwen.html"
    base = "https://www.mhwmm.com"

    headers = {"User-Agent": "Mozilla/5.0"}

    r = requests.get(url, headers=headers, timeout=15)
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
    return list(dict.fromkeys(urls))


# =========================
# 🚀 主程序
# =========================
async def main():

    init(BOT_TOKEN)

    # 📌 读取频道
    channels = load_channels(CSV_URL)
    sent = load_sent()

    print(f"✅ 频道数量：{len(channels)}")

    if not channels:
        print("❌ 没有频道")
        return

    pool = get_pool()

    # 📌 过滤已发送
    pool = [u for u in pool if not is_sent(u)]

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

        # 🔥 防止 Telegram 限速
        await asyncio.sleep(1)


# =========================
# 🚀 入口
# =========================
if __name__ == "__main__":
    asyncio.run(main())

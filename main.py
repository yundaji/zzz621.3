import asyncio
from fetch import get_article
from tg import init, send_post
from utils import load_channels, load_sent, save_sent
from config import BOT_TOKEN, CSV_URL


# =========================
# 🧠 全站文章池
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

    return list(dict.fromkeys(urls))


# =========================
# 🚀 主程序
# =========================
async def main():

    init(BOT_TOKEN)

    channels = load_channels(CSV_URL)
    sent = load_sent()

    print(f"频道数量：{len(channels)}")

    if not channels:
        print("❌ 没有频道")
        return

    # =========================
    # 📌 关键：过滤已发送
    # =========================
    pool = [u for u in get_pool() if u not in sent]

    if not pool:
        print("没有可用文章")
        return

    # =========================
    # 🔥 核心：每个频道分配不同文章
    # =========================
    article_index = 0
    pool_len = len(pool)

    for channel in channels:

        channel_name = channel["channel"]
        count = int(channel.get("count", 1))

        for _ in range(count):

            if article_index >= pool_len:
                print("⚠️ 文章不够分配")
                break

            url = pool[article_index]
            article_index += 1

            article = get_article(url)

            print(f"发送：{url} -> {channel_name}")

            try:
                await send_post(channel_name, article)

                print(f"✅ 成功：{channel_name}")

                save_sent(url)

            except Exception as e:
                print(f"❌ 失败：{channel_name} -> {e}")

        await asyncio.sleep(1)


# =========================
# 🚀 启动
# =========================
if __name__ == "__main__":
    asyncio.run(main())

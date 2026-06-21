import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import random


BASE_DOMAIN = "https://www.mhwmm.com"


# =========================
# ❌ 过滤垃圾文本
# =========================
def is_bad_text(text: str) -> bool:
    bad_keywords = [
        "Copyright",
        "版权所有",
        "ICP备案",
        "扫描关注",
        "微信公众号",
        "邮箱",
        "mhwmm.com",
        "缅华网",
        "伊江树报道",
        "来源",
        "十一新闻周刊"
    ]
    return any(k in text for k in bad_keywords)


# =========================
# 📌 获取文章列表
# =========================
def get_article_list():
    url = "https://www.mhwmm.com/miandianxinwen.html"

    headers = {"User-Agent": "Mozilla/5.0"}

    r = requests.get(url, headers=headers, timeout=15)
    r.encoding = "utf-8"

    soup = BeautifulSoup(r.text, "lxml")

    links = []

    for a in soup.find_all("a"):
        href = a.get("href")

        if not href:
            continue

        if "miandianxinwen" not in href:
            continue

        full_url = urljoin(BASE_DOMAIN, href)
        links.append(full_url)

    return list(dict.fromkeys(links))


# =========================
# 📰 获取文章内容 + 随机图片
# =========================
def get_article(url):
    headers = {"User-Agent": "Mozilla/5.0"}

    r = requests.get(url, headers=headers, timeout=15)
    r.encoding = "utf-8"

    soup = BeautifulSoup(r.text, "lxml")

    # =========================
    # 🧾 标题
    # =========================
    title = soup.title.text.strip() if soup.title else ""

    # =========================
    # 🧹 清理无关标签
    # =========================
    for tag in soup(["script", "style", "footer", "nav", "header", "form", "aside"]):
        tag.decompose()

    # =========================
    # 🧠 正文（保留）
    # =========================
    content = []

    for p in soup.find_all("p"):
        text = p.get_text(strip=True)

        if not text:
            continue

        if len(text) < 5:
            continue

        if is_bad_text(text):
            continue

        content.append(text)

    # 去尾部垃圾
    while content and is_bad_text(content[-1]):
        content.pop()

    text = "\n".join(content)

    # =========================
    # 🖼 随机图片（核心修复）
    # =========================
    images = []

    for img in soup.find_all("img"):
        src = img.get("src") or img.get("data-src")

        if not src:
            continue

        src_lower = src.lower()

        # ❌ 过滤无关图片
        if any(x in src_lower for x in ["logo", "icon", "avatar", "qr", "wechat", "banner"]):
            continue

        # ❌ base64
        if "data:image" in src_lower:
            continue

        # ✅ 补全 URL
        if src.startswith("//"):
            src = "https:" + src
        else:
            src = urljoin(BASE_DOMAIN, src)

        images.append(src)

    # 去重
    images = list(dict.fromkeys(images))

    # 🔥 随机打乱（关键）
    random.shuffle(images)

    # 每篇最多3张随机图
    images = images[:3]

    return {
        "title": title,
        "text": text[:4000],
        "images": images,
        "url": url
    }

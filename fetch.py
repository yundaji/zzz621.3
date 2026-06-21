import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


BASE_DOMAIN = "https://www.mhwmm.com"


# =========================
# ❌ 过滤垃圾文字
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

        # 只保留新闻链接
        if "miandianxinwen" not in href:
            continue

        full_url = urljoin(BASE_DOMAIN, href)
        links.append(full_url)

    # 去重
    return list(dict.fromkeys(links))


# =========================
# 📰 获取文章正文 + 图片
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
    # 🧹 清理无关结构
    # =========================
    for tag in soup(["script", "style", "footer", "nav", "header", "form", "aside"]):
        tag.decompose()

    # =========================
    # 🧠 正文提取
    # =========================
    content = []

    # 优先抓 p 标签
    for p in soup.find_all("p"):
        text = p.get_text(strip=True)

        if not text:
            continue

        if len(text) < 5:
            continue

        if is_bad_text(text):
            continue

        content.append(text)

    # 去掉尾部垃圾（版权/来源）
    while content and is_bad_text(content[-1]):
        content.pop()

    text = "\n".join(content)

    # =========================
    # 🖼 正文图片（核心修复）
    # =========================
    images = []

    # 只在正文结构内找图片（更精准）
    for block in soup.find_all(["p", "div"]):

        for img in block.find_all("img"):
            src = img.get("src") or img.get("data-src")

            if not src:
                continue

            src_lower = src.lower()

            # ❌ 过滤无关图片
            if any(x in src_lower for x in ["logo", "icon", "avatar", "qr", "wechat", "banner"]):
                continue

            # ❌ base64 / 占位图
            if "data:image" in src_lower or "base64" in src_lower:
                continue

            # ✅ 补全链接
            if src.startswith("//"):
                src = "https:" + src
            else:
                src = urljoin(BASE_DOMAIN, src)

            images.append(src)

    # 去重
    images = list(dict.fromkeys(images))

    return {
        "title": title,
        "text": text[:4000],
        "images": images[:3],
        "url": url
    }

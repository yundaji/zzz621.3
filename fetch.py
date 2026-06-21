import requests
from bs4 import BeautifulSoup


def clean_text(text):
    """过滤底部垃圾内容"""
    bad_keywords = [
        "Copyright",
        "版权所有",
        "ICP备案",
        "扫描关注",
        "微信公众号",
        "邮箱",
        "mhwmm.com",
        "十一新闻周刊"
    ]

    return not any(k in text for k in bad_keywords)


def get_article(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    r = requests.get(url, headers=headers, timeout=15)
    r.encoding = "utf-8"

    soup = BeautifulSoup(r.text, "lxml")

    # 标题
    title = soup.title.text.strip() if soup.title else ""

    # 删除无用结构
    for tag in soup(["script", "style", "footer", "nav", "header", "form", "aside"]):
        tag.decompose()

    # =========================
    # ✅ 正文提取（核心优化）
    # =========================
    content_parts = []

    # 优先抓 p 标签
    for p in soup.find_all("p"):
        text = p.get_text(strip=True)

        if not text:
            continue

        if not clean_text(text):
            continue

        # 过滤太短的垃圾行
        if len(text) < 5:
            continue

        content_parts.append(text)

    text = "\n".join(content_parts)

    # =========================
    # 🖼 图片提取
    # =========================
    images = []

    for img in soup.find_all("img"):
        src = img.get("src")
        if not src:
            continue

        if "logo" in src or "icon" in src:
            continue

        if src.startswith("/"):
            src = "https://www.mhwmm.com" + src

        images.append(src)

    # 去重
    images = list(dict.fromkeys(images))

    return {
        "title": title,
        "text": text[:4000],
        "images": images[:3],
        "url": url
    }

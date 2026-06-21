import requests
from bs4 import BeautifulSoup


def get_article(url):
    r = requests.get(url, timeout=15)
    soup = BeautifulSoup(r.text, "lxml")

    # 标题
    title = soup.title.text.strip() if soup.title else ""

    # ❌ 去掉无用内容（关键）
    for tag in soup(["script", "style", "footer", "nav"]):
        tag.decompose()

    # ✅ 正文（只取 p 标签）
    paragraphs = soup.select("p")
    text = "\n".join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))

    # ❌ 过滤无效图片
    images = []
    for img in soup.select("img"):
        src = img.get("src")
        if not src:
            continue
        if "logo" in src or "icon" in src:
            continue
        if src.startswith("/"):
            src = "https://www.mhwmm.com" + src
        images.append(src)

    return {
        "title": title,
        "text": text[:4000],
        "images": images[:3],
        "url": url
    }

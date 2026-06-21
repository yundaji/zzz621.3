import requests
from bs4 import BeautifulSoup


def is_bad_text(text: str) -> bool:
    """过滤底部署名/广告/版权"""
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


def get_article(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    r = requests.get(url, headers=headers, timeout=15)
    r.encoding = "utf-8"

    soup = BeautifulSoup(r.text, "lxml")

    # 标题
    title = soup.title.text.strip() if soup.title else ""

    # 删除无关结构
    for tag in soup(["script", "style", "footer", "nav", "header", "form", "aside"]):
        tag.decompose()

    # =========================
    # 🧠 正文提取（核心）
    # =========================
    content = []

    for p in soup.find_all("p"):
        text = p.get_text(strip=True)

        if not text:
            continue

        # 过滤垃圾
        if is_bad_text(text):
            continue

        if len(text) < 5:
            continue

        content.append(text)

    # =========================
    # 🔥 去掉尾部签名（重点强化）
    # =========================
    while content:
        last = content[-1]
        if is_bad_text(last):
            content.pop()
        else:
            break

    text = "\n".join(content)

    # =========================
    # 🖼 正文图片（精准版）
    # =========================
    images = []

    for img in soup.find_all("img"):
        src = img.get("src") or img.get("data-src")

        if not src:
            continue

        # ❌ 过滤无关图
        if "logo" in src or "icon" in src or "avatar" in src:
            continue

        # ✅ 只保留正文上传图
        if "/uploads/" not in src:
            continue

        # 补全 URL
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

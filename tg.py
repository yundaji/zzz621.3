from telegram import Bot
import asyncio

bot = None


def init(token):
    global bot
    bot = Bot(token=token)


async def send_post(channel, article):
    text = f"{article['text']}"

    # 只发图片 + 正文
    if article["images"]:
        media = article["images"][0]
        await bot.send_photo(
            chat_id=channel,
            photo=media,
            caption=text[:1024]
        )
    else:
        await bot.send_message(chat_id=channel, text=text)

from email import message
import logging

import requests
from bs4 import BeautifulSoup


from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


async def search_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.message.text

    URL = f"https://asaxiy.uz/product?key={query}"
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")

    search_items = soup.find("div", class_="row custom-gutter mb-40")
    #print(search_items)

    items = search_items.find_all("div", class_='col-6', recursive=False)[:10]
    #print(items)

    for item in items:
        img_div = item.find('div', class_='product__item-img')
        #print(img_div)
        img = img_div.find('img')['data-src']
        if img[-5:]==".webp":
            img=img[:-5]
        #print(img)
        info = item.find('div',class_='product__item-info')
        #print(info)

        title = info.find('h5', class_='product__item__info-title').text
        #print(title)
        
        narx = info.find('span', class_='product__item-price').text
        #print(narx)

        text = f"Nomi:{title.strip()} \nNarx:{narx.strip()}\n"
        #print(text)


        await context.bot.send_photo(update.message.chat_id, photo=img, caption=text)


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("1779735646:AAFoPa_0mMrsAdj7B7t9VLSzLeMeUlpk-E0").build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_handler))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
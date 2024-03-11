from newsdataapi import NewsDataApiClient
from typing import Final
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes, Application

TOKEN: Final = '7017203647:AAGyjotiPJGOYNVxY4r1M-r97VV7SRuS1Ag'
API_KEY: Final = 'pub_3912528cdd15f7bd599255a186b90566fc632'
API_URL: Final = 'https://newsdata.io/api/1/news?apikey=pub_3912528cdd15f7bd599255a186b90566fc632'
BOT_USERNAME: Final = '@DailyNewsBot_bot'


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_message = (
        "Hello! I'm a news bot. You can use the following commands:\n"
        "/newses - Obtener noticias en español.\n"
        "/newsen - Get news in English."
    )
    await update.message.reply_text(help_message)


async def get_news_data_from_api(update: Update, context: ContextTypes.DEFAULT_TYPE, language: str, country: str):
    if language == 'en':
        await update.message.reply_text("Getting news data in english")

    else:
        await update.message.reply_text("Obteniendo datos de noticias en español")

    api = NewsDataApiClient(API_KEY)
    res = api.news_api(country=country, language=language)
    if 'results' in res:
        news_data = res['results']
        for article in news_data:
            message = (f"📰 {article.get('title', 'N/A')}\n\n"
                       f"{article.get('description', 'N/A')}\n\n"
                       f"{article.get('link', 'N/A')}\n\n"
                       f"{article.get('source_url', 'N/A')}")
            message_parts = await split_message(message)

            # Enviar cada parte del mensaje al usuario
            for part in message_parts:
                await update.message.reply_text(part)
    else:
        await update.message.reply_text("Lo siento, no se pudieron obtener los datos de noticias en español")


async def news_english(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await get_news_data_from_api(update, context, 'en', 'us')


async def news_spanish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await get_news_data_from_api(update, context, 'es', 'es')


async def split_message(message: str):
    """
            This method splits in parts the message because Telegram
            has a limit of 4096 characters.
    """
    return [message[i:i + 4096] for i in range(0, len(message), 4096)]


if __name__ == '__main__':
    print("Starting bot...")

    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler('newses', news_spanish))
    app.add_handler(CommandHandler('newsen', news_english))
    app.add_handler(CommandHandler('start', start))

    print("Polling...")
    app.run_polling()

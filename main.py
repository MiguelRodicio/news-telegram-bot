import aiohttp
import httpx
import requests
from typing import Final
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, ContextTypes, CallbackContext, Application
import asyncio

# Crear una cola asyncio
update_queue = asyncio.Queue()

TOKEN: Final = '7017203647:AAGyjotiPJGOYNVxY4r1M-r97VV7SRuS1Ag'
API_KEY: Final = 'pub_3912528cdd15f7bd599255a186b90566fc632'
API_URL: Final = 'https://newsdata.io/api/1/news?apikey=pub_3912528cdd15f7bd599255a186b90566fc632'
BOT_USERNAME: Final = '@DailyNewsBot_bot'


async def get_api_data():
    async with httpx.AsyncClient() as client:
        response = await client.get(API_URL, params={'apikey': API_KEY})

        if response.status_code == 200:
            data = response.json()
            if 'results' in data:
                return data['results']
            else:
                print("Error: 'results' key not found in API response")
                return []
        else:
            print("Error obtaining data from API:", response.status_code)
            return []


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi! I am DailyNewsBot")
    news_data = await get_api_data()

    if news_data:
        # Iterar sobre cada artículo
        for article in news_data:
            # Construir el mensaje con los detalles del artículo
            message = (f"📰 {article.get('title', 'N/A')}\n\n"
                       f"Description: {article.get('description', 'N/A')}\n\n"
                       f"Link: {article.get('link', 'N/A')}\n\n"
                       f"Source URL: {article.get('source_url', 'N/A')}")
            # Enviar el mensaje al usuario
            await update.message.reply_text(message)
    else:
        await update.message.reply_text("Lo siento, no se pudieron obtener los datos de noticias")


if __name__ == '__main__':
    print("Starting bot...")

    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler('start', start_command))

    print("Polling...")
    app.run_polling()

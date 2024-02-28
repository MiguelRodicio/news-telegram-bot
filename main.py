from typing import Final
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, ContextTypes, CallbackContext

TOKEN: Final = '7017203647:AAGyjotiPJGOYNVxY4r1M-r97VV7SRuS1Ag'
BOT_USERNAME: Final = '@DailyNewsBot_bot'


async def start_command(update: Update, context: ContextTypes):
    await update.message.reply_text("Hi! I am DailyNewsBot")

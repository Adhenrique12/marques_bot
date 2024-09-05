from telegram import Update
from telegram.ext import CallbackContext

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Olá! Eu sou seu bot.')

async def help(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Aqui estão os comandos disponíveis...')

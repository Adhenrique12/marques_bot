from telegram.ext import Application, CommandHandler
from config import TOKEN
from bot import handlers

def main():
    application = Application.builder().token(TOKEN).build()

    # Registrar comandos
    application.add_handler(CommandHandler("start", handlers.start))
    application.add_handler(CommandHandler("help", handlers.help))

    # Iniciar o bot
    application.run_polling()

if __name__ == '__main__':
    main()

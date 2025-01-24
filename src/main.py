import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    CommandHandler,
    filters,
    ContextTypes
)
from dotenv import load_dotenv
import os
import openai
from bot.telegram_bot import process_group_message

load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)




TOKEN = os.getenv('TELEGRAM_TOKEN')

def main():
    logging.info("Iniciando la aplicación de Telegram...")
    
    application = ApplicationBuilder().token(TOKEN).build()
    logging.info("Aplicación de Telegram creada con éxito.")
    
    text_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, process_group_message)
    
    application.add_handler(text_handler)
    
    logging.info("Handlers registrados. Iniciando el polling...")
    
    application.run_polling()
    
    logging.info("Aplicación finalizada.")

if __name__ == '__main__':
    main()

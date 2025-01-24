import logging
from telegram import Update
from telegram.ext import ContextTypes
from openai_chat.openai_client import extract_intro_data
from muvinai.utilities.init_creds import init_gspread
from pprint import pprint

gc = init_gspread()

logger = logging.getLogger(__name__)

async def process_group_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.message.from_user.full_name
    user_text = update.message.text

    logger.info(f"Mensaje recibido de {user}: {user_text}")

    extracted_data = extract_intro_data(user_text)

    if extracted_data:
        logger.info(f"Datos extraídos correctamente: {extracted_data}")

        row_data = [
            user,
            extracted_data.get("Intro", ""),
            extracted_data.get("From", ""),
            extracted_data.get("Passion", ""),
            extracted_data.get("SomethingFun", "")
        ]
        
        wks = gc.open_by_key("1V2UYw2uYFskFoYP4pquwf2ylop7Qeqa2dmzoBZ9AL3Q").sheet1
        wks.append_row(row_data)
       
    else:
        logger.debug("El mensaje no parece ser una introducción estructurada.")

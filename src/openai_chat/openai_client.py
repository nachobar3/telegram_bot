from openai import OpenAI
import logging
import os
from dotenv import load_dotenv


load_dotenv()

logger = logging.getLogger(__name__)

openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)



def extract_intro_data(user_text):
    """
    Usa OpenAI para analizar si un mensaje sigue la estructura de introducción y extraer los datos clave.
    Retorna un diccionario con las secciones esperadas o None si no es una introducción válida.
    """
    prompt = f"""
    Eres un asistente que extrae información estructurada de presentaciones de usuarios en un grupo de Telegram.
    Si el mensaje sigue la estructura de una presentación, responde en formato JSON con las siguientes claves:
    
    {{
      "Intro": "Texto de la introducción",
      "From": "Lugar de origen",
      "Passion": "Pasión o interés principal",
      "SomethingFun": "Algo divertido sobre la persona"
    }}

    Si el mensaje **no** es una presentación, responde con `null`. Además, comprime la información de cada campo para mantener
    sólo lo relevante. Excluye textos como "Hello! I'm Petar, and i ...", 

    Mensaje recibido:
    "{user_text}"

    Respuesta JSON:
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": prompt}],
            temperature=0.2
        )
        
        result = response.choices[0].message.content.strip()

        
        # Intentar convertir a JSON
        import json
        parsed_data = json.loads(result)
        
        if isinstance(parsed_data, dict):
            return parsed_data  # Retorna el JSON estructurado
        else:
            return None  # No es una presentación válida
        
    except Exception as e:
        logger.error(f"Error procesando mensaje con OpenAI: {e}")
        return None

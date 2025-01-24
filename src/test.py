from openai import OpenAI
import os
from dotenv import load_dotenv


load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)


# Obtener la lista de modelos disponibles
models = client.models.list()

for model in models.data:
    print(model.id)

import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')

chat_id = 1248172018
message = 'This is a notification '
url = 'https://api.telegram.org/bot%s/sendMessage?chat_id=%s' % (
    f'{API_TOKEN}', f'{chat_id}')
_ = requests.post(url, json={'text': f'{message}'}, timeout=10)

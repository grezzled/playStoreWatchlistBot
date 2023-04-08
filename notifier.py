import requests

chat_id = 1248172018
token = '6060583785:AAEpBspgwL7eGSK5OZR-9fLHdYwGvkJ2JwQ'
message = 'This is a notification '
url = 'https://api.telegram.org/bot%s/sendMessage?chat_id=%s' % (
    f'{token}', f'{chat_id}')
_ = requests.post(url, json={'text': f'{message}'}, timeout=10)

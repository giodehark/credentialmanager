import requests


def mandar_mensajebot(mensaje, token, chat_id):
    send_text = 'https://api.telegram.org/bot' + token + '/sendMessage?chat_id=' + chat_id + '&parse_mode=Markdown&text=' + mensaje
    response = requests.post(send_text)
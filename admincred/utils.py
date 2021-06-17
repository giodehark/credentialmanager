import random
import string

import requests


def randomString(stringLength):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


def generar_token():
    tam_token = 12
    token = randomString(tam_token)
    return token


def mandar_mensajebot(token, chat_id):
    print(token, chat_id)
    bot_token = "1710714751:AAFX0qrHpLByoXfqNAvy6FUCop6cjP_QxaM"
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + chat_id + '&parse_mode=Markdown&text=' + token
    response = requests.get(send_text)



def deleteToken(profiletoken):
    profiletoken.token = ""
    print("Entró la función de eliminar token")
    print(profiletoken.user.username)
    profiletoken.save()

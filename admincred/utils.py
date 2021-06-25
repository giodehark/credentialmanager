from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os
import base64
import sys
from getpass import getpass
import random
import string
import requests
from django.contrib.auth.models import User


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

def generarIv():
    iv = os.urandom(16)
    return iv

def generar_llave_aes_from_password(password):
    password = password.encode('utf-8')
    derived_key = HKDF(algorithm=hashes.SHA256(),
                       length=32,
                       salt=None,
                       info=b'handshake data ',
                       backend=default_backend()).derive(password)
    return derived_key



def cifrarDatos(datos, iv, llave_aes):
    print(datos)
    print('iv encodebase64',iv)
    print(llave_aes)
    aesCipher = Cipher(algorithms.AES(llave_aes), modes.CTR(iv),
                       backend=default_backend())
    cifrador = aesCipher.encryptor()
    cifrado = cifrador.update(datos)
    cifrador.finalize()
    return cifrado


def descifrar(cifrado, llave_aes, iv):
    print('tipos de datos',cifrado, type(cifrado),llave_aes, type(llave_aes),iv, type(iv))
    aesCipher = Cipher(algorithms.AES(llave_aes), modes.CTR(iv),
                       backend=default_backend())
    descifrador = aesCipher.decryptor()
    plano = descifrador.update(cifrado)
    descifrador.finalize()
    return plano

#def obtenerId():
    #username = request.user.username
    #userid = User.objects.get(username=username)
    #return userid
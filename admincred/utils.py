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
    '''Se crea un string con una longitud determinada utilizando letras'''
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


def generar_token():
    '''Se genera un token de longitud de 12 el cual se regresara'''
    tam_token = 12
    token = randomString(tam_token)
    return token


def mandar_mensajebot(token, chat_id):
    '''Se enviara un mensaje por medio del bot con el token, al usuario que quiere iniciar sesion por medio del id_chat que
    registro  '''
    print(token, chat_id)
    bot_token = "1710714751:AAFX0qrHpLByoXfqNAvy6FUCop6cjP_QxaM"
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + chat_id + '&parse_mode=Markdown&text=' + token
    response = requests.get(send_text)



def deleteToken(profiletoken):
    '''Se eliminara el token que esta registrado en la base de datos '''
    profiletoken.token = ""
    print("Entró la función de eliminar token")
    print(profiletoken.user.username)
    profiletoken.save()

def generarIv():
    '''Se generara un vector de inicializacion random de longitud de 16 el cual se regresara '''
    iv = os.urandom(16)
    return iv

def generar_llave_aes_from_password(password):
    '''Se generara una llave aes por medio de la expansion de una password la cual sera la del usuario
    y se regresara para ser utilizada para el cifrado'''
    password = password.encode('utf-8')
    derived_key = HKDF(algorithm=hashes.SHA256(),
                       length=32,
                       salt=None,
                       info=b'handshake data ',
                       backend=default_backend()).derive(password)
    return derived_key



def cifrarDatos(datos, iv, llave_aes):
    '''Se cifra el dato proporciona utilizando el cifrado simetrico aes por medio de un vector de inicializacion
    y una llave aes'''

    aesCipher = Cipher(algorithms.AES(llave_aes), modes.CTR(iv),
                       backend=default_backend())
    cifrador = aesCipher.encryptor()
    cifrado = cifrador.update(datos)
    cifrador.finalize()
    return cifrado


def descifrar(cifrado, llave_aes, iv):
    '''En la siguiente funcion  se reciben los tres datos necesarios en binario y se realiza
    descifrado simetro de un dato que estaba cifrado '''
    print('tipos de datos',cifrado, type(cifrado),llave_aes, type(llave_aes),iv, type(iv))
    aesCipher = Cipher(algorithms.AES(llave_aes), modes.CTR(iv),
                       backend=default_backend())
    descifrador = aesCipher.decryptor()
    plano = descifrador.update(cifrado)
    descifrador.finalize()
    return plano


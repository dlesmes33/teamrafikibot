from Info_Mensaje import Info_Mensaje
from Registro import Registro
import json
import Servicios
import datetime
import os
import requests
from flask import Flask, request
from datetime import datetime,time
import Persona


BOT_URL = f'https://api.telegram.org/bot{os.environ["BOT_KEY"]}/'  # <-- add your telegram token as environment variable

app = Flask(__name__)

servicio = Servicios.Servicios()

paso = 0

@app.route('/',methods=['Post'])
def main():
        sms = request.json
        info = info_mensaje(sms)
		lista =[]
        print(sms)
        
        if not info.is_bot and info.tipo_sms == "texto":
            if info.id_persona in lista:
                texto = str(leer_mensaje(sms)).lower()
                 if info.id_persona == '877561784':
                    if paso == 0:
                       a=0
                    elif paso == 1:
                        a = 0
                    elif paso == 1:
                        a = 0
                    elif paso == 1:
                        a = 0
                    elif paso == 1:
                        a = 0
                    elif paso == 1:
                        a = 0
                    elif paso == 1:
                        a = 0
                    elif paso == 1:
                        a = 0
                    elif paso == 1:
                        a = 0
                    elif paso == 1:
                        a = 0
                    elif paso == 1:
                        a = 0
                    elif paso == 1:
                        a = 0
                    elif paso == 1:
                        a = 0
                 else:



                 str(leer_mensaje(sms)).lower() == "!polerank":
            if info.id_persona == '877561784':

            if str(leer_mensaje(sms)).lower() == "!polerank":
             

        return ''

def leer_mensaje(mensaje):
    texto = mensaje['message']['text']
    return texto

def str_puntuacion(lista):
    result = "Puntos 💜"+ "\n"
    for i in lista:
        nombre = i.nombre_persona
        puntos = i.cantidad
        result = result + nombre + "-->"
        result = result + str(puntos) + "\n"
    return result

def enviar_mensaje(idChat, texto):
    json_data = {
        "chat_id": idChat,
        "text": texto,
    }
    message_url = BOT_URL + 'sendMessage'
    requests.post(message_url, json=json_data)
    return ''

def info_mensaje(mensaje):
    tipo_sms = "texto_editado"
    tipo_chat = None
    chat = None
    update_id = None
    persona = None
    id_persona = None
    bot = None 
    id_chat = None
    date = None
    if "message" in mensaje:
        if "text" in mensaje["message"]:
            tipo_sms ="texto"
        elif "sticker" in  mensaje["message"]:
            tipo_sms = "sticker"
        elif "animation" in mensaje["message"]:
            tipo_sms = "animacion"
        elif "photo" in mensaje["message"]:
            tipo_sms = "foto"
        else:
            tipo_sms = "otro"
        
        tipo_chat = mensaje['message']['chat']['type']

        chat = ""
        if not tipo_chat.lower() == "private":
            chat = mensaje['message']['chat']['title']
        else:
            chat = tipo_chat

        update_id = mensaje['update_id']
        persona = mensaje['message']['from']['first_name']
        id_persona = mensaje['message']['from']['id']
        bot = mensaje['message']['from']['is_bot']
        id_chat = mensaje['message']['chat']['id']
        date = mensaje['message']['date']
    return Info_Mensaje( persona, id_persona , bot, chat, id_chat, tipo_chat, tipo_sms, date,update_id)



def unix_date(fecha):
        return datetime.fromtimestamp(fecha).time()





    

if __name__ == '__main__':  
        app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)

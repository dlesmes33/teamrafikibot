from Info_Mensaje import Info_Mensaje
import json
import Servicios
import datetime
import os
import requests
from flask import Flask, request
from datetime import datetime,time



BOT_URL = f'https://api.telegram.org/bot{os.environ["BOT_KEY"]}/'  # <-- add your telegram token as environment variable

app = Flask(__name__)

servicio = Servicios.Servicios()

paso = 0
parametro1 = None
parametro2 = None
parametro3 = None



@app.route('/',methods=['Post'])
def main():
        paso = 0
        sms = request.json
        info = info_mensaje(sms)
        lista = ['877561784']
        print(sms)
        if not info.is_bot and info.tipo_sms == "texto":
            texto = str(leer_mensaje(sms)).lower()
            if texto == "/agregar":
                servicio.insertar_persona(33,"pene")
                enviar_mensaje(info.id_chat, "Insertado")
            elif texto == "/prestar":
                enviar_mensaje(info.id_chat, "Escriba el nombre del que va a prestar")
            elif texto == "/rotar":
                enviar_mensaje(info.id_chat, "Rotando...")
            elif texto == "/imprimir":
                aux = servicio.imprimir_personas()
                enviar_mensaje(info.id_chat,aux)
			elif texto == "/poninas@TeamRafikiBot":
			    poninas = "¿Qué son estas poninas?"+"\n"+"Las poninas son una estrategia creada con el fin de beneficiar a todos los miembros del equipo que participen en las mismas. Los participantes cada vez que se pueda se unirán y le harán prestados al miembro del equipo de turno para que este se pueda comprar un nuevo paquete de 15. Una vez comprado el paquete, el miembro beneficiado procederá a devolver el dinero que le fue prestado y posteriormente se unirá al resto para ayudar a otro miembro colocándose de último en la cola para recibir nuevos préstamos. Los préstamos se harán en forma de rotación."
                enviar_mensaje(info.id_chat,poninas)
			elif texto == "/beneficios":
			    beneficios = "¿Qué beneficios trae?"+"\n"+"Con esta estrategia cada participante podrá aumentar su capital invertido independientemente de si logra tener referidos o no, además no tendrá que esperar los 5 meses para comprarse un nuevo paquete por el mismo (Al final todos hemos entrado con paquetes de $15 y sin conseguir referidos habría que esperar esos 5 meses para poder comenzar a hacer interés compuesto en solitario)"
                enviar_mensaje(info.id_chat,beneficios)	
        return ''

def leer_mensaje(mensaje):
    texto = mensaje['message']['text']
    return texto

def str_puntuacion(lista):
    result = "Puntos ðŸ’œ"+ "\n"
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

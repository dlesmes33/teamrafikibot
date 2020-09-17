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
@app.route('/',methods=['Post'])
def main():
    paso = servicio.get_variable("paso")
    sms = request.json
    info = info_mensaje(sms)
    lista = [837689725]

    print(sms)

    if not info.is_bot and info.tipo_sms == "texto":
        if info.id_persona in lista:

            texto = str(leer_mensaje(sms)).lower()
            if info.id_persona == 837689725:
                if paso == "0":
                    if texto == "/agregar":
                        servicio.set_variable("paso","1")
                        enviar_mensaje(info.id_chat, "Escriba el nombre de usuario")

                    elif texto == "/prestar":
                        servicio.set_variable("paso","3")
                        enviar_mensaje(info.id_chat, "Escriba el nombre del que va a prestar")

                    elif texto == "/rotar":

                        enviar_mensaje(info.id_chat, "Rotando...")

                    elif texto == "/rotar":

                        enviar_mensaje(info.id_chat, "Rotando...")

                    elif texto == "/esc":
                        servicio.set_variable("paso", "3")

                        enviar_mensaje(info.id_chat, "Inicio...")


                elif paso == "1":
                    lista_un = servicio.lista_de_personas()
                    if not texto in lista_un:
                        servicio.set_variable("p1",texto)
                        servicio.set_variable("paso","2")
                        enviar_mensaje(info.id_chat, "Escriba el id del usuario en telegram")
                    else:

                        enviar_mensaje(info.id_chat, "Ese usuario ya esta registrado intentelo de nuevo o escriba /esc para salir")

                elif paso == "2":
                    if not texto in lista:

                        servicio.insertar_persona(servicio.get_variable("p1"), texto)
                        enviar_mensaje(info.id_chat, "Operación realizada")
                        servicio.set_variable("paso", "0")
                        servicio.set_variable("p1", "None")
                    else:

                        enviar_mensaje(info.id_chat, "Ese id ya esta registrado \n Escriba /esc para salir")




                elif paso == 3:
                    lista_un = servicio.lista_de_personas()
                    if texto in lista_un:
                        servicio.set_variable("p1", texto)
                        enviar_mensaje(info.id_chat, "Escribe el nombre de usuario del que va a recibir")
                        servicio.set_variable("paso", "4")
                    else:
                        enviar_mensaje(info.id_chat, "No")



                elif paso == "4":
                     servicio.set_variable("p2", texto)
                     enviar_mensaje(info.id_chat, "Escribe la cantidad del monto")
                     servicio.set_variable("paso", "5")


                elif paso == 5:

                    servicio.prestar(servicio.get_variable("p1"),servicio.get_variable("p2"),float(texto))
                    enviar_mensaje(info.id_chat, "Operacion realizada.")
                    servicio.set_variable("paso", "0")







    return ''



'''
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
        return ''
'''
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

def obtener_alias():
    return ""

def unix_date(fecha):
        return datetime.fromtimestamp(fecha).time()





    

if __name__ == '__main__':  
        app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)

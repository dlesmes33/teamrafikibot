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
    lista = servicio.lista_de_id()

    print(sms)
    print("Mayor len es: "+servicio.mayor_len())
    if not info.is_bot and info.tipo_sms == "texto":
        if str(info.id_persona) in lista:
            alias = servicio.cambio_alias(info.username, str(info.id_persona))
            if alias == "None":
                enviar_mencionar(info.id_chat, "Por favor, edite su perfil y elija un nombre de usuario: ", info.persona, info.id_persona)
            else:
                enviar_mensaje(info.id_chat,alias)


            texto = str(leer_mensaje(sms)).lower()


            if info.id_persona == 877561784:

                if texto == "/cancelar" or texto == "/cancelar@teamrafikibot":
                    servicio.set_variable("paso", "0")
                    enviar_mensaje(info.id_chat, "Operación cancelada")
                elif paso == "0":
                    if texto == "/agregar_usuario" or texto == "/agregar_usuario@teamrafikibot":
                        servicio.set_variable("paso","1")
                        enviar_mensaje(info.id_chat, "Escriba el nombre de usuario")

                    elif texto == "/prestar" or texto == "/prestar@teamrafikibot":
                        servicio.set_variable("paso","3")
                        enviar_mensaje(info.id_chat, "Escriba el nombre del que va a prestar")

                    elif texto == "/rotar" or texto == "/rotar@teamrafikibot":
                        enviar_mensaje(info.id_chat, "Rotando...")
                        servicio.rotar()
                        enviar_mensaje(info.id_chat, "Operación realizada")

                    elif texto == "/agregar_paquete" or texto == "/agregar_paquete@teamrafikibot":
                        enviar_mensaje(info.id_chat, "Escriba el alias del dueño del paquete:")
                        servicio.set_variable("paso", "6")

                    elif texto == "/wallets" or texto == "/wallets@teamrafikibot":
                        enviar_mensaje(info.id_chat,mostrar_wallets())

                    else:
                       reporte =  reportes(texto)
                       if not reporte == "":
                           enviar_mensaje(info.id_chat,reporte)
                       else:
                           comando_especiales(info, texto)



                elif paso == "1":
                    lista_un = servicio.lista_de_personas()

                    if not texto in lista_un:
                        if not servicio.validar_nombreUsuario(texto):
                            enviar_mensaje(info.id_chat,"Por favor introduzca correctamente el nombre de usuario de la persona que quiere agregar o escriba /cancelar para salir")
                            paso = "1.5"
                            servicio.set_variable("paso","1.5")
                        if paso == "1":
                            servicio.set_variable("p1",texto)
                            servicio.set_variable("paso","2")
                            enviar_mensaje(info.id_chat, "Escriba el id del usuario en telegram")
                    else:

                        enviar_mensaje(info.id_chat, "Ese usuario ya esta registrado intentelo de nuevo o escriba /cancelar para salir")

                elif paso == "1.5":
                    lista_un = servicio.lista_de_personas()
                    if not texto in lista_un:
                        if not servicio.validar_nombreUsuario(texto):
                            enviar_mensaje(info.id_chat,"Por favor introduzca correctamente el nombre de usuario de la persona que quiere agregar o escriba /cancelar para salir")
                        else:
                            servicio.set_variable("p1", texto)
                            servicio.set_variable("paso", "2")
                            enviar_mensaje(info.id_chat, "Escriba el id del usuario en telegram")
                    else:
                        enviar_mensaje(info.id_chat,"Ese usuario ya esta registrado intentelo de nuevo o escriba /cancelar para salir")

                elif paso == "2":
                    if not texto in lista:

                        servicio.set_variable("p2",texto)
                        enviar_mensaje(info.id_chat, "Va ha hacer el registro de:\nusuario: "+servicio.get_variable("p1")+"\nid_telegram: "+
                                       servicio.get_variable("p2")+"\nEscriba ok para continuar o /cancelar para cancelar")
                        servicio.set_variable("paso", "2.5")

                    else:

                        enviar_mensaje(info.id_chat, "Ese id ya esta registrado \n Escriba /cancelar para salir")

                elif paso == "2.5":
                    if not texto in lista:

                        servicio.insertar_persona(servicio.get_variable("p1"),servicio.get_variable("p2") )
                        enviar_mensaje(info.id_chat, "Operación realizada")
                        servicio.set_variable("paso", "0")
                        servicio.set_variable("p1", "None")
                    else:

                        enviar_mensaje(info.id_chat, "Ese id ya esta registrado \n Escriba /cancelar para salir")




                elif paso == "3":
                    lista_un = servicio.lista_de_personas()
                    if texto in lista_un:
                        servicio.set_variable("p1", texto)
                        enviar_mensaje(info.id_chat, "Escribe el nombre de usuario del que va a recibir")
                        servicio.set_variable("paso", "4")
                    else:
                        enviar_mensaje(info.id_chat, "Ese usuario no esta registrado intente de nuevo o /cancelar para salir")



                elif paso == "4":
                    lista_un = servicio.lista_de_personas()
                    if texto in lista_un:
                       servicio.set_variable("p2", texto)
                       enviar_mensaje(info.id_chat, "Escribe la cantidad del monto")
                       servicio.set_variable("paso", "5")
                    else:
                        enviar_mensaje(info.id_chat,
                                       "Ese usuario no esta registrado intente de nuevo o /cancelar para salir")


                elif paso == "5":
                    num = servicio.to_float(texto)
                    if not num == -1:
                        servicio.set_variable("p3", texto)

                        enviar_mensaje(info.id_chat, "Va a realizar un prestamo desde: "+servicio.get_variable("p1")+" hacia: "+servicio.get_variable("p2")+" por un valor de "+servicio.get_variable("p3")+"\n"+"Presione cualquier cosa para continuar o /cancelar para salir")
                        servicio.set_variable("paso", "5.6")
                    else:
                        enviar_mensaje(info.id_chat,"El numero debe ser positivo y '.'para marcar los decimales intente de nuevo o /cancelar para salir")

                elif paso == "5.6":
                    enviar_mensaje(info.id_chat, "Prestando...")
                    servicio.prestar(servicio.get_variable("p1"), servicio.get_variable("p2"), float(servicio.get_variable("p3")))
                    enviar_mensaje(info.id_chat, "Operacion realizada.")
                    servicio.set_variable("paso", "0")

                elif paso == "6":
                    lista_un = servicio.lista_de_personas()
                    if texto in lista_un:
                       servicio.set_variable("p1", texto)
                       enviar_mensaje(info.id_chat, "Escribe el tipo de paquete")
                       servicio.set_variable("paso", "7")
                    else:
                        enviar_mensaje(info.id_chat,
                                       "Ese usuario no esta registrado intente de nuevo o /cancelar para salir")

                elif paso == "7":

                    if servicio.validar_paquete(texto):
                       servicio.set_variable("p2", texto)
                       enviar_mensaje(info.id_chat, "Escribe la fecha de compra \n Formato: \n dd/mm/aaaa")
                       servicio.set_variable("paso", "8")
                    else:
                        enviar_mensaje(info.id_chat,
                                       "Ese paquete no esta ofertado por la empresa intente de nuevo o /cancelar para salir")

                elif paso == "8":
                    fecha = servicio.fecha(texto)
                    if not fecha == "-1":
                        servicio.set_variable("p3", fecha)
                        enviar_mensaje(info.id_chat, "Va a registraar el paquete /cancelar")
                        servicio.set_variable("paso", "8.5")
                    else:
                        enviar_mensaje(info.id_chat,"Por favor ingrese la fecha de compra con el formato correcto o /cancelar para salir")

                elif paso == "8.5":
                    enviar_mensaje(info.id_chat, "Insertando...")
                    servicio.insertar_paquete(servicio.get_variable("p1"),servicio.get_variable("p2"),servicio.get_variable("p3"))
                    enviar_mensaje(info.id_chat, "Operacion realizada")
                    servicio.set_variable("paso", "0")

            else:
                warn  = advertencia(texto)
                if not advertencia == "":
                    enviar_mensaje(info.id_chat, warn)
                reporte = reportes(texto)
                if not  reporte == "":
                    enviar_mensaje(info.id_chat, reporte)
                else:
                    comando_especiales(info,texto)

        else:
            text = str(leer_mensaje(sms)).lower()
            enviar_mensaje(info.id_chat,"Usted no está registrado"+"\n"+"Para más información entre a este grupo"+"\n"+"\n"+"Team rafiki No Registrados"+"\n"+"https://t.me/joinchat/AAAAAFFkD3as9fTMvGuQWw")
            if not info.username == None:
                   enviar_mensaje(877561784,info.username +"\n"+text)
            else:
                   enviar_mencionar(877561784,text,info.persona,info.id_persona)
    return ''


def reportes(comando):

    if comando == "/llamar" or comando == "/llamar@teamrafikibot":
        texto = ListaOrganizada()

    elif comando == "/poninas" or comando == "/poninas@teamrafikibot":
        texto = "Que son estas poninas?"+"\n"+"Las poninas son una estrategia creada con el fin de beneficiar a todos los miembros del equipo que participen en las mismas. Los participantes cada vez que se pueda se uniran y le haran prestados al miembro del equipo de turno para que este se pueda comprar un nuevo paquete de 15. Una vez comprado el paquete, el miembro beneficiado procedera a devolver el dinero que le fue prestado y posteriormente se unira al resto para ayudar a otro miembro colocandose de ultimo en la cola para recibir nuevos prestamos. Los prestamos se haran en forma de rotacion."

    elif comando == "/beneficios" or comando =="/beneficios@teamrafikibot":
        texto = "Que beneficios trae?"+"\n"+"Con esta estrategia cada participante podra aumentar su capital invertido independientemente de si logra tener referidos o no, ademas no tendra que esperar los 5 meses para comprarse un nuevo paquete por el mismo (Al final todos hemos entrado con paquetes de $15 y sin conseguir referidos habra que esperar esos 5 meses para poder comenzar a hacer interes compuesto en solitario)"
	
    elif comando == "/meta" or comando == "/meta@teamrafikibot":
         texto ="¿Cuál sería inicialmente la meta?"+"\n"+"La meta inicial es que cada miembro llegue a la suma de $75 dólares invertidos (5 paquetes de 15), ya que de esta forma sus ganancias mensuales serán aproximadamente de $15 dólares por lo que podrá hacer interés compuesto y así aumentar sus ganancias exponencialmente, pues cada mes podrá comprar un nuevo paquete de 15. Esto no significa que una vez cumplida la meta el miembro tendría que retirarse de las poninas " 
    elif comando == "/interes_compuesto" or comando == "/interes_compuesto@teamrafikibot":
         texto ="¿Qué es el interés compuesto?"+"\n"+"El interés compuesto consiste en reinvertir tus ganancias siempre que puedas y de esta forma aumentar exponencialmente tus ganancias cada vez que puedas y al tener más capital invertido, al mes siguiente tener mayores ganancias."
    elif comando == "/rotacion" or comando == "/rotacion@teamrafikibot":
         texto = rotacion()
    elif comando == "/bots" or comando == "/bots@teamrafikibot":
         texto = "Bots:"+"\n"+"@Trustinvestingschool_bot"+"\n"+"@TrustInvestingEnCuba_bot"
    elif comando == "/prestamos" or comando == "/prestamos@teamrafikibot":
        texto = mostrar_prestamos()
    elif comando == "/paquetes_comprados" or comando == "/paquetes_comprados@teamrafikibot":
        texto = mostrar_paquetes()
    elif comando == "/paquetes_por_fecha" or comando == "/paquetes_por_fecha@teamrafikibot":
        texto = mostrar_paquetes_por_fecha()
    elif comando == "/paquetes_vencidos" or comando == "/paquetes_vencidos@teamrafikibot":
        texto = mostrar_paquetes_vencidos()
    else:
        texto =""

    return texto

def advertencia(texto):
    warn = ""
    comandos = ["/cancelar","/cancelar@teamrafikibot",
                "/agregar_usuario","/agregar_usuario@teamrafikibot",
                "/prestar","/prestar@teamrafikibot",
                "/rotar","/rotar@teamrafikibot",
                "/agregar_paquete","/agregar_paquete@teamrafikibot",
                "/wallets","/wallets@teamrafikibot"]

    if texto in comandos:
        warn = "Usted no tiene acceso a usar el comando "+texto

    return warn

def comando_especiales(info,texto):
    comando_wallet(info,texto)

def comando_wallet(info,texto):
    alias_wallet = servicio.wallet_usuario(texto)
    if not alias_wallet == -2:
        if not alias_wallet == -1:
            alias, wallet = alias_wallet
            mostrar_wallet_usuario(info.id_chat, alias, wallet)
    else:
        enviar_mensaje(info.id_chat, "Ese usuario no está registrado")

def ListaOrganizada():
    texto = ""
    if not servicio.lista_de_personas().__len__() == 0:
        for nombre in servicio.lista_de_personas():
            texto += nombre + "\n"
    else:
        texto = "No hay ningún usuario registrado en este momento"
    return texto

def rotacion():
    texto = ""
    for nombre in servicio.lista_de_personas_orden_rotacion():
        texto += str(nombre[1])+" - "+nombre[0] + "\n"

    texto += "El proximo miembro en beneficiarse es el: "+servicio.get_variable("persona_actual_rotacion")
    return texto

def mostrar_prestamos():
    texto =""
    prestamos =  servicio.lista_prestamos()
    personas = servicio.lista_serials_usuario()
    actual = ""
    if not prestamos.__len__() == 0:
        for desde, para, cantidad in prestamos:
            desde = servicio.buscar_usuario_por_serial(personas, desde)
            para = servicio.buscar_usuario_por_serial(personas, para)
            if not para == actual:
                texto += "\n"+para + " ha recibido un préstamo de :\n"
                texto += desde + "($" + cantidad + ")" + "\n"
                actual = para
            else:
                texto += desde + "($" + cantidad + ")" + "\n"
    else:
        texto = "No hay préstamos vigentes en este momento"
    return texto

def mostrar_paquetes():
    texto =""
    cantidad = []
    del_ususario = []
    paquetes =  servicio.lista_paquete()
    print(paquetes)
    personas = servicio.lista_serials_usuario()
    actual = ""
    if not paquetes.__len__() == 0:
        for usuario, tipo in paquetes:
            usuario = servicio.buscar_usuario_por_serial(personas, usuario)
            if not usuario == actual:
                if not actual == "":
                    texto += actual + ":\n"
                    for i in range(0, cantidad.__len__()):
                        texto += "Tipo: " + str(del_ususario[i]) + " Cantidad: " + str(cantidad[i]) + "\n"

                cantidad = [1]
                del_ususario = [tipo]

                actual = usuario
            else:
                posicion = buscar_paquete(del_ususario, tipo)
                if not posicion == -1:
                    cantidad[posicion] += 1
                else:
                    del_ususario += [tipo]
                    cantidad += [1]

        texto += actual + ":\n"
        for i in range(0, cantidad.__len__()):
            texto += "Tipo: " + str(del_ususario[i]) + " Cantidad: " + str(cantidad[i]) + "\n"
    else:
        texto = "No hay ningún paquete comprado en este momento"

    return texto

def buscar_paquete(lista, paquete):
    i =0
    existe = -1
    while existe == -1 and i < len(lista):
        if paquete == lista[i]:
            existe = i
        i += 1
    return existe

def mostrar_paquetes_por_fecha():
    texto = ""
    paquetes = servicio.lista_paquetes_fechas()
    if not paquetes.__len__() == 0:
        for nombre,fecha,tipo in paquetes:
            texto += nombre + "  " + str(fecha) + "  " + str(tipo) + "\n"
    else:
        texto = "No hay ningún paquete comprado en este momento"
    return texto

def mostrar_paquetes_vencidos():
    texto = ""
    paquetes = servicio.lista_paquetes_vencidos()
    if not paquetes.__len__() == 0:
        for nombre, fecha, tipo in paquetes:
            texto += nombre + "  "+str(fecha)+"  "+str(tipo)+"\n"
    else:
        texto = "No hay ningún paquete vencido en este momento"
    return texto

def mostrar_wallets():
    texto = ""
    wallets = servicio.lista_wallets()
    if not wallets.__len__() == 0:
        for nombre,wallet in wallets:
            texto += nombre + "\n" + wallet +"\n"+"\n"
    else:
        texto = "No hay ninguna wallet registrada en este momento"
    return texto




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
			elif texto == "/poninas@TeamRafikiBot":
			    poninas = "�Qu� son estas poninas?"+"\n"+"Las poninas son una estrategia creada con el fin de beneficiar a todos los miembros del equipo que participen en las mismas. Los participantes cada vez que se pueda se unir�n y le har�n prestados al miembro del equipo de turno para que este se pueda comprar un nuevo paquete de 15. Una vez comprado el paquete, el miembro beneficiado proceder� a devolver el dinero que le fue prestado y posteriormente se unir� al resto para ayudar a otro miembro coloc�ndose de �ltimo en la cola para recibir nuevos pr�stamos. Los pr�stamos se har�n en forma de rotaci�n."
                enviar_mensaje(info.id_chat,poninas)
			elif texto == "/beneficios":
			    beneficios = "�Qu� beneficios trae?"+"\n"+"Con esta estrategia cada participante podr� aumentar su capital invertido independientemente de si logra tener referidos o no, adem�s no tendr� que esperar los 5 meses para comprarse un nuevo paquete por el mismo (Al final todos hemos entrado con paquetes de $15 y sin conseguir referidos habr�a que esperar esos 5 meses para poder comenzar a hacer inter�s compuesto en solitario)"
                enviar_mensaje(info.id_chat,beneficios)	
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


def enviar_mencionar(idChat, texto,nick,id):
    json_data = {
        "chat_id": idChat,
        "text": texto + nick,
        'entities': [{'offset': len(texto), 'length': len(nick), 'type': 'text_mention', 'user': {'id': id, 'is_bot': False, 'first_name': nick}}]
    }

    message_url = BOT_URL + 'sendMessage'
    requests.post(message_url, json=json_data)
    return ''

def mostrar_wallet_usuario(id_chat,alias,wallet):
    if not wallet == None:
        texto = "Wallet de " + alias + "\n"
        json_data = {
            "chat_id": id_chat,
            "text": texto + wallet,
            'entities': [{'offset': len(texto), 'length': len(wallet), 'type': 'code'}]
        }

        message_url = BOT_URL + 'sendMessage'
        requests.post(message_url, json=json_data)
    else:
       enviar_mensaje(id_chat,"El usuario "+alias+" no tiene wallet registrada")
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
    username = None
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
        if "username" in mensaje["message"]['from']:
           username ="@" + mensaje['message']['from']['username']
    return Info_Mensaje(persona, id_persona , bot, chat, id_chat, tipo_chat, tipo_sms, date, update_id, username)

def obtener_alias():
    return ""

def unix_date(fecha):
        return datetime.fromtimestamp(fecha).time()





    

if __name__ == '__main__':  
        app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)

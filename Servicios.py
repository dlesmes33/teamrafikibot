from Persona import Persona
import sys,psycopg2
import Singleton
import Conexion
import  datetime

@Singleton.SingletonDecorator
class Servicios():
    def insertar_persona(self, username,  id_telegram  ):
        c = Conexion.Conexion()
        miCursor = c.miConexion.cursor()
        param_list = [username , id_telegram]
        miCursor.execute("INSERT INTO usuario(nombre_usuario,id_telegram) VALUES (%s, %s)", param_list)
        c.miConexion.commit()
        miCursor.close()

    def imprimir_personas(self):
        c = Conexion.Conexion()
        miCursor = c.miConexion.cursor()
        miCursor.execute("SELECT * FROM usuario")
        tabla = miCursor.fetchall() 
        puntos = []
        for row in tabla:
            persona = str(row[0]) + " " + str(row[1]) + str(row[2])
            puntos.append(persona)
        miCursor.close()
        return puntos

    def existe_prestamo(self , desde , para):
        existe = -1
        c = Conexion.Conexion()

        miCursor = c.miConexion.cursor()
        param_list = [desde, para]
        miCursor.execute("SELECT id_prestamo FROM public.prestamo WHERE desde = %s AND para = %s",param_list)
        tabla = miCursor.fetchall()
        for row in tabla:
             existe = row[0]

        miCursor.close()
        return existe

    def monto_prestamo(self, id_prestamo):
        existe = -1
        c = Conexion.Conexion()

        miCursor = c.miConexion.cursor()
        param_list = [id_prestamo]
        miCursor.execute("SELECT  cantidad FROM public.prestamo WHERE id_prestamo = %s ",param_list)
        tabla = miCursor.fetchall()
        for row in tabla:
             existe = row[0]

        miCursor.close()
        return existe

    def prestar(self,desde_un, para_un , cantidad):
        desde = self.get_userId(desde_un)
        para = self.get_userId(para_un)
        texto = ""

        id_prestamo_ida = self.existe_prestamo(desde, para)
        id_prestamo_vuelta = self.existe_prestamo(para, desde)
        if not id_prestamo_ida == -1:
            self.sumar(id_prestamo_ida, cantidad)
            texto = "Se ha aumentado el prestamo desde: "+desde_un+" hacia :"+para_un+"."

        elif id_prestamo_vuelta == -1:
            self.insertar_prestamo(desde , para, cantidad)
            texto = "Se ha registrado un prestamo desde: " + desde_un + " hacia :" + para_un + "."

        else:
            monto = float(self.monto_prestamo(id_prestamo_vuelta))
            if monto == cantidad:
                self.eliminar(id_prestamo_vuelta)
                texto = "Se ha eliminado un prestamo desde: " + para_un + " hacia :" + desde_un + "."
            elif monto > cantidad:
                self.restar(id_prestamo_vuelta, cantidad)
                texto = "Se ha devuelto una parte desde: " + para_un + " hacia :" + desde_un + "."
            elif monto < cantidad:
                self.eliminar(id_prestamo_vuelta)
                self.insertar_prestamo(desde , para, cantidad - monto)
                texto = "Se ha realizado un prestamo desde: " + desde_un + " hacia :" + para_un + "."

        return texto




    def get_variable(self, nombre):
        c = Conexion.Conexion()

        miCursor = c.miConexion.cursor()
        param_list = [nombre]
        miCursor.execute("SELECT  valor FROM public.variable WHERE nombre = %s ", param_list)
        tabla = miCursor.fetchall()
        for row in tabla:
            existe = row[0]
        miCursor.close()
        return existe

    def set_variable(self, nombre, valor):
        c = Conexion.Conexion()
        miCursor = c.miConexion.cursor()
        param_list = [ valor, nombre,]
        miCursor.execute("Update variable set valor = %s where nombre = %s", param_list)
        c.miConexion.commit()
        miCursor.close()

    def get_userId(self, username):
        c = Conexion.Conexion()

        miCursor = c.miConexion.cursor()
        param_list = [username]
        miCursor.execute("SELECT  id_usuario FROM public.usuario WHERE nombre_usuario = %s ", param_list)
        tabla = miCursor.fetchall()
        for row in tabla:
            existe = row[0]
        miCursor.close()
        return existe


    def lista_de_personas(self):
        c = Conexion.Conexion()

        miCursor = c.miConexion.cursor()

        miCursor.execute("SELECT  nombre_usuario FROM usuario ORDER BY id_usuario")
        tabla = miCursor.fetchall()
        personas = []
        for row in tabla:
            personas += [row[0]]
        miCursor.close()
        return personas

    def lista_de_id(self):
        c = Conexion.Conexion()

        miCursor = c.miConexion.cursor()

        miCursor.execute("SELECT  id_telegram FROM usuario ")
        tabla = miCursor.fetchall()
        personas = []
        for row in tabla:
            personas += [row[0]]
        miCursor.close()
        return personas

    def to_float(self, cadena):
        try:
            num = float(cadena)
            if num < 0:
                num = -1
            return num
        except ValueError:
            return -1

    def validar_nombreUsuario(self ,cadena="@a"):
        estado = False
        un = cadena[1:]
        print("validando: "+un)
        if cadena[0] == '@' and un.__len__() > 4 and un.isidentifier():
            estado = True
        return estado

    def castear_cantidad_prestamo (self, id_prestamo):
        c = Conexion.Conexion()
        miCursor = c.miConexion.cursor()
        param_list = [id_prestamo]
        miCursor.execute("SELECT cantidad  FROM prestamo  WHERE id_prestamo = %s", param_list)
        tabla = miCursor.fetchall()
        for row in tabla:
            cantidad_casteada = float(row[0])
        miCursor.close()
        return cantidad_casteada



    def sumar(self, id_prestamo, cantidad):
        c = Conexion.Conexion()
        miCursor = c.miConexion.cursor()
        cantidad_casteada = self.castear_cantidad_prestamo(id_prestamo)
        cantidad_casteada += cantidad
        param_list = [cantidad_casteada, id_prestamo]
        miCursor.execute("UPDATE prestamo   SET cantidad = %s  WHERE id_prestamo = %s", param_list)
        c.miConexion.commit()
        miCursor.close()

    def restar(self, id_prestamo, cantidad):
        c = Conexion.Conexion()
        miCursor = c.miConexion.cursor()
        cantidad_casteada = self.castear_cantidad_prestamo(id_prestamo)
        cantidad_casteada -= cantidad
        param_list = [cantidad_casteada, id_prestamo]
        miCursor.execute("UPDATE prestamo   SET cantidad = %s  WHERE id_prestamo = %s", param_list)
        c.miConexion.commit()
        miCursor.close()

    def eliminar(self, id_prestamo):
        c = Conexion.Conexion()
        miCursor = c.miConexion.cursor()
        param_list = [id_prestamo]
        miCursor.execute("Delete FROM public.prestamo WHERE id_prestamo = %s", param_list)
        c.miConexion.commit()
        miCursor.close()

    def insertar_prestamo(self, desde , para, cantidad):
        c = Conexion.Conexion()
        miCursor = c.miConexion.cursor()
        param_list = [ desde , para, cantidad]
        miCursor.execute("INSERT INTO prestamo(desde,para,cantidad) VALUES (%s, %s,%s)", param_list)
        c.miConexion.commit()
        miCursor.close()

    def rotar(self):
         c = Conexion.Conexion()
         miCursor = c.miConexion.cursor()
         persona_actual = int(self.get_variable("persona_actual_rotacion"))
         miCursor.execute("SELECT COUNT(orden_rotacion) AS cantidad_personas_rotacion FROM public.usuario;")
         tabla = miCursor.fetchall()

         for row in tabla:
             cant_personas = row[0]
             miCursor.close()
             if persona_actual == cant_personas:
                nuevo_actual = 1

             else:
                 nuevo_actual = persona_actual + 1

             self.set_variable("persona_actual_rotacion", nuevo_actual)

    def lista_de_personas_orden_rotacion(self):
        c = Conexion.Conexion()
        miCursor = c.miConexion.cursor()
        miCursor.execute("SELECT  nombre_usuario,orden_rotacion FROM usuario WHERE orden_rotacion IS NOT NULL ORDER BY orden_rotacion")
        tabla = miCursor.fetchall()
        personas = []
        for row in tabla:
            personas += [row]
        miCursor.close()
        print("*****************")
        print(personas)
        return personas
    def validar_paquete(self,cadena ):
        bien = False
        paquetes = [15,30,60,100,300,500,1000,2000,5000,10000,50000,100000]
        try:
            num = int(cadena)
            if num in paquetes:
                bien = True
        except ValueError:
                bien = False

        return bien


    def fecha(self, cadena="02/12/2009"):
        try:
            if not cadena.__len__() == 10:
                raise TypeError

            dias_mes = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

            anno_actual = datetime.datetime.today().year
            d = cadena[0:2]
            m = cadena[3:5]
            a = cadena[6:10]
            dia = int(d)
            mes = int(m)
            anno = int(a)
            # ver si el año es biciesto
            if not cadena[2] == "/" or not cadena[5] == "/":
                raise TypeError
            if mes < 0 or mes > 12:
                raise ValueError
            if anno < 2019 or anno > anno_actual:
                raise ValueError
            if ((anno % 4 == 0 and anno % 100 != 0) or anno % 400 == 0):
                dias_mes[1] += 1
            if dia < 0 or dia > dias_mes[mes - 1]:
                raise ValueError


        except TypeError:
            return "-1"
        except ValueError:
            return "-1"


        return str(anno) + "-" + str(mes) + "-" + str(dia)

    def lista_serials_usuario(self):
        c = Conexion.Conexion()
        miCursor = c.miConexion.cursor()
        miCursor.execute("SELECT  id_usuario,nombre_usuario FROM usuario ")
        tabla = miCursor.fetchall()
        personas = []
        for row in tabla:
            personas += [row]
        miCursor.close()
        print("*****************")
        print(personas)
        return personas

    def lista_prestamos(self):
        c = Conexion.Conexion()
        miCursor = c.miConexion.cursor()
        miCursor.execute("SELECT  desde,para,cantidad FROM prestamo ORDER BY para")
        tabla = miCursor.fetchall()
        prestamos = []
        for row in tabla:
            prestamos += [row]
        miCursor.close()
        print("*****************")
        print(prestamos)
        return prestamos

    def buscar_usuario_por_serial(self,personas,serial):
        for id,nombre  in personas:
            if id == serial:
                return nombre
        return "Kasper"

    def lista_paquete(self):
        c = Conexion.Conexion()
        miCursor = c.miConexion.cursor()
        miCursor.execute("SELECT fk_usuario,tipo FROM paquete WHERE activo = TRUE  ORDER BY fk_usuario ASC, tipo ASC")
        tabla = miCursor.fetchall()
        paquetes = []
        for row in tabla:
            paquetes += [row]
        miCursor.close()
        print("*****************")
        print(paquetes)
        return paquetes

    def lista_paquetes_fechas(self):
        c = Conexion.Conexion()
        miCursor = c.miConexion.cursor()
        miCursor.execute("SELECT nombre_usuario,fecha,tipo FROM paquete JOIN usuario ON id_usuario = fk_usuario WHERE activo = TRUE  ORDER BY fecha")
        tabla = miCursor.fetchall()
        paquetes = []
        for row in tabla:
            paquetes += [row]
        miCursor.close()
        return paquetes

    def lista_paquetes_vencidos(self):
        c = Conexion.Conexion()
        miCursor = c.miConexion.cursor()
        miCursor.execute(
            "SELECT nombre_usuario,fecha,tipo FROM paquete JOIN usuario ON id_usuario = fk_usuario WHERE activo = FALSE  ORDER BY fecha")
        tabla = miCursor.fetchall()
        paquetes = []
        for row in tabla:
            paquetes += [row]
        miCursor.close()
        return paquetes

    def lista_wallets(self):
        c = Conexion.Conexion()
        miCursor = c.miConexion.cursor()
        miCursor.execute("SELECT nombre_usuario,wallet FROM usuario WHERE wallet IS NOT NULL  ORDER BY id_usuario")
        tabla = miCursor.fetchall()
        wallets = []
        for row in tabla:
            wallets += [row]
        miCursor.close()
        return wallets

    def insertar_paquete(self, username,  paquete, fecha  ):
        c = Conexion.Conexion()
        miCursor = c.miConexion.cursor()
        usuario = self.get_userId(username)

        param_list = [usuario, paquete , fecha]
        miCursor.execute("INSERT INTO paquete(fk_usuario,tipo,fecha) VALUES (%s, %s, %s)", param_list)
        c.miConexion.commit()
        miCursor.close()

    def cambio_alias (self,alias_actual,id_telegram):
        try:
            texto = ""
            c = Conexion.Conexion()
            miCursor = c.miConexion.cursor()
            param_list = [id_telegram]
            miCursor.execute("SELECT nombre_usuario FROM usuario WHERE id_telegram = %s  ", param_list)
            tabla = miCursor.fetchall()
            for row in tabla:
              nombre_usuario = row[0]
            if not alias_actual == nombre_usuario:
                texto ="#CambioDeNombreDeUsuario"+"\n"+"El usuario "+alias_actual+" ha cambiado su nombre de usuario:"+"\n"+"Su nombre de usuario anterior era "+nombre_usuario
                print("NUevo: "+alias_actual)
                print("Viejo: " + nombre_usuario)
                print("ID tele"+id_telegram)
                param_list = [alias_actual,id_telegram]
                miCursor.execute("UPDATE usuario SET nombre_usuario = %s WHERE id_telegram = %s",param_list)
                c.miConexion.commit()
            miCursor.close()
            return texto
        except:
            return "None"

    def reconocer_comando(self,texto="/comando"):
        retorno = ""
        comando = texto[0:22]
        print("reconocer comando " + comando)
        if comando == "/wallet@teamrafikibot":
            retorno = "/wallet"
        else:
            comando = texto[0:7]
            if comando == "/wallet":
                retorno = "/wallet"
        print("retornando " + retorno)
        return retorno

    def wallet_usuario(self, texto=""):
        comando = self.reconocer_comando(texto)
        wallet = ""
        print("comando: " + comando)
        if comando == "/wallet":
            alias = texto[8:]
            print("alias: " + alias)
            if not alias == "":
                if self.validar_nombreUsuario(alias):
                    lista_un = self.lista_de_personas()

                    for alias_temp in lista_un:
                        print("for alias temp " + str(alias_temp).lower())
                        print("for alias " + alias)
                        if alias == str(alias_temp).lower():                           
                            c = Conexion.Conexion()
                            miCursor = c.miConexion.cursor()
                            param_list = [alias_temp]
                            miCursor.execute("SELECT wallet FROM usuario WHERE LOWER(nombre_usuario) = %s", param_list)
                            tabla = miCursor.fetchall()

                            for row in tabla:
                                wallet = row[0]
                            miCursor.close()
                            print("wallet fresquita" + wallet)
                            if not wallet == "":
                                print("wallet " + wallet)
                                print("alias " + alias_temp)
                                wallet_alias = alias_temp, wallet
                                return wallet_alias

    def validar_id(self,text =""):
        resto = text[1:]
        if (not text[0].isdigit() and not text[0] == '-')or len(text) < 7:
            return False
        for c in resto:
            if not c.isdigit():
                return False
        return True


    def wallet_usuario(self,texto=""):
        comando = self.reconocer_comando(texto)
        print("comando: "+comando)
        if comando == "/wallet":
            alias = texto[8:]
            print("alias: "+alias)
            lista_un = self.lista_de_personas()
            usuario_encontrado = False
            for alias_temp in lista_un:
                print("for alias temp " + str(alias_temp).lower())
                print("for alias " + alias)
                if alias == str(alias_temp).lower():
                    usuario_encontrado = True
                    c = Conexion.Conexion()
                    miCursor = c.miConexion.cursor()
                    param_list = [alias_temp]
                    miCursor.execute("SELECT wallet FROM usuario WHERE LOWER(nombre_usuario) = %s", param_list)
                    tabla = miCursor.fetchall()
                    wallet = ""
                    for row in tabla:
                        wallet = row[0]
                    miCursor.close()
                if usuario_encontrado:
                    if not wallet == "":
                        print("wallet " + wallet)
                        print("alias " + alias_temp)
                        wallet_alias = alias_temp, wallet
                        return wallet_alias

                else:
                    return "No encontrado"


        else:
            return "/wallet"
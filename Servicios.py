from Persona import Persona
import sys, psycopg2
import Singleton
import Conexion

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
            self.insertar(desde , para, cantidad)
            texto = "Se ha registrado un prestamo desde: " + desde_un + " hacia :" + para_un + "."

        else:
            monto = self.monto_prestamo(id_prestamo_vuelta)
            if monto == cantidad:
                self.eliminar(id_prestamo_vuelta)
                texto = "Se ha eliminado un prestamo desde: " + para_un + " hacia :" + desde_un + "."
            elif monto > cantidad:
                self.restar(id_prestamo_vuelta, cantidad)
                texto = "Se ha devuelto una parte desde: " + para_un + " hacia :" + desde_un + "."
            elif monto < cantidad:
                self.eliminar(id_prestamo_vuelta)
                self.insertar(desde , para, cantidad - monto)
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

        miCursor.execute("SELECT  nombre_usuario FROM usuario ")
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
        print(un)
        if cadena[0] == '@' and un.__len__() > 4 and un.isidentifier():
            estado = True
        return estado








    def sumar(self, id_prestamo, cantidad):
        c = Conexion.Conexion()
        miCursor = c.miConexion.cursor()
        param_list = [ cantidad, id_prestamo]
        miCursor.execute("Update prestamo   Set cantidad = cantidad + %s  where id_prestamo = %s", param_list)
        c.miConexion.commit()
        miCursor.close()

    def restar(self, id_prestamo, cantidad):
        c = Conexion.Conexion()
        miCursor = c.miConexion.cursor()
        param_list = [cantidad, id_prestamo]
        miCursor.execute("Update prestamo   Set cantidad = cantidad - %s  where id_prestamo = %s", param_list)
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
         miCursor.execute("SELECT COUNT(orden_rotacion) FROM public.usuario WHERE orden_rotacion != null;")
         tabla = miCursor.fetchall()

         for row in tabla:
             cant_personas = row[0]
             miCursor.close()
             if persona_actual == cant_personas:
                nuevo_actual = 1

             else:
                 nuevo_actual = persona_actual + 1

             self.set_variable("persona_actual_rotacion", nuevo_actual)




	
    '''
    def puntuacion(self,grupo):
        c = Conexion.Conexion()
        miCursor = c.miConexion.cursor()
        param_list = [grupo]
        miCursor.execute("SELECT * FROM pole JOIN persona ON persona.id_persona = pole.id_persona WHERE pole.id_grupo = %s ORDER BY pole.cantidad DESC",param_list)
        tabla = miCursor.fetchall() 
        puntos = []
        for row in tabla:
            persona = Persona(grupo=row[0], id=row[1], cant=row[2],nombre_persona=row[5])
            puntos.append(persona)
        miCursor.close()
        return puntos

    def persona_en_grupo(self,grupo,persona):
        existe = False
        c = Conexion.Conexion()
        miCursor = c.miConexion.cursor()
        param_list = [grupo,persona]
        miCursor.execute("SELECT * FROM pole WHERE pole.id_grupo = %s AND pole.id_persona = %s",param_list)
        tabla = miCursor.fetchall()
        for row in tabla:
            existe = True
            break
        miCursor.close()
        return existe

    def existe_grupo(self,grupo):
        existe = False
        c = Conexion.Conexion()
        miCursor = c.miConexion.cursor()
        param_list = [grupo]
        miCursor.execute("SELECT pole.cantidad FROM pole WHERE pole.id_grupo = %s",param_list)
        tabla = miCursor.fetchall() 
        for row in tabla:
            existe = True
        miCursor.close()
        return existe
        

    def annadir_persona_pole(self,grupo, persona):
        c = Conexion.Conexion()
        miCursor = c.miConexion.cursor()
        param_list = [grupo,persona,1]
        miCursor.execute("INSERT INTO pole (id_grupo,id_persona,cantidad)VALUES(%s,%s,%s)",param_list)
        c.miConexion.commit()
        miCursor.close()

    def annadir_persona(self,id,nombre):
        c = Conexion.Conexion()
        miCursor = c.miConexion.cursor()
        param_list = [id,nombre]
        miCursor.execute("INSERT INTO persona(id_persona,nombre_persona)VALUES(%s,%s)",param_list)
        c.miConexion.commit()
        miCursor.close()

    def actualizar_persona(self,id,nombre):
        c = Conexion.Conexion()
        miCursor = c.miConexion.cursor()
        param_list = [nombre,id]
        miCursor.execute("UPDATE persona SET nombre_persona = %s WHERE persona.id_persona = %s",param_list)
        c.miConexion.commit()
        miCursor.close()

    def punto(self,grupo,persona):
        c = Conexion.Conexion()
        miCursor = c.miConexion.cursor()
        param_list = [grupo,persona]
        miCursor.execute("UPDATE pole SET cantidad = cantidad + 1 WHERE pole.id_grupo = %s AND pole.id_persona = %s",param_list)
        c.miConexion.commit()
        miCursor.close()

    def add_pole(self,grupo, persona):
        if self.existe_grupo(grupo):
            if self.persona_en_grupo(grupo, persona):
                self.punto(grupo, persona)
            else:
                self.annadir_persona_pole(grupo, persona)
        else:
            self.annadir_persona_pole(grupo, persona)

    def pole(self,info):
        gana = False
        id = info.id_chat
        if not self.esta_grupo_registro(id):
            self.annadir_grupo_registro(id)
            gana = True
        return gana

    def esta_grupo_registro(self,id_grupo):
        existe = False
        c = Conexion.Conexion()
        miCursor = c.miConexion.cursor()
        param_list = [id_grupo]
        miCursor.execute("SELECT * FROM registro WHERE registro.id_grupo = %s",param_list)
        tabla = miCursor.fetchall() 
        for row in tabla:
            existe = True
        miCursor.close()
        return existe

    def annadir_grupo_registro(self,id_grupo):
        c = Conexion.Conexion()
        miCursor = c.miConexion.cursor()
        param_list = [id_grupo]
        miCursor.execute("INSERT INTO registro(id_grupo)VALUES(%s)",param_list)
        c.miConexion.commit()
        miCursor.close()

    def clean_registro(self):
        c = Conexion.Conexion()
        miCursor = c.miConexion.cursor()
        miCursor.execute("DELETE from registro")
        c.miConexion.commit()
        miCursor.close()

    def update_num_pole(self,numero):
        c = Conexion.Conexion()
        miCursor = c.miConexion.cursor()
        param_list = [numero]
        miCursor.execute("UPDATE num_pole SET numero_pole = %s",param_list)
        c.miConexion.commit()
        miCursor.close()

    def obtener_num_pole(self):
        num_pole = 30
        c = Conexion.Conexion()
        miCursor = c.miConexion.cursor()
        miCursor.execute("SELECT * FROM num_pole")
        tabla = miCursor.fetchall() 
        for row in tabla:
            num_pole = row[0]
        c.miConexion.commit()
        miCursor.close()
        return num_pole

    def analizarPersona(self,id_persona,nombre_persona):
        if self.tengo_persona(id_persona):
            self.actualizar_persona(id_persona,nombre_persona)
        else:
            self.annadir_persona(id_persona,nombre_persona)

    def tengo_persona(self,id_persona):
        existe = False
        c = Conexion.Conexion()
        miCursor = c.miConexion.cursor()
        param_list = [id_persona]
        miCursor.execute("SELECT * FROM persona WHERE id_persona = %s",param_list)
        tabla = miCursor.fetchall() 
        for row in tabla:
            existe = True
        miCursor.close()
        return existe

    def existe_prestamo(self , desde , para):
        existe = -1
        c = Conexion.Conexion()

        miCursor = c.miConexion.cursor()
        param_list = [desde, para]
        miCursor.execute("SELECT id_prestamo, desde, para, cantidad FROM public.prestamo WHERE desde = %s AND para = %s",param_list)
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

    def prestar(self,desde, para , cantidad):

        id_prestamo = self.existe_prestamo(desde, para)
        if not id_prestamo == -1:
            self.sumar(id_prestamo,cantidad)
            return "Se ha aumentado el prestamo desde: "+desde+" hacia :"+para+"."

        else :
            self.insertar(desde , para, cantidad)
            return "Se ha registrado un prestamo desde: " + desde + " hacia :" + para + "."

        id_prestamo = self.existe_prestamo(para, desde)
        if not id_prestamo == -1:
            monto = self.monto_prestamo(id_prestamo)
            if monto == cantidad:
                self.eliminar(id_prestamo)

            elif monto > cantidad:
                self.restar(id_prestamo, cantidad)
            elif monto < cantidad:
                self.eliminar(id_prestamo)
                self.insertar(desde , para, cantidad - monto )







    def sumar(self, id_prestamo, cantidad):
        c = Conexion.Conexion()
        miCursor = c.miConexion.cursor()
        param_list = [ cantidad, id_prestamo]
        miCursor.execute("Update prestamo   Set cantidad = cantidad + %s  where id_prestamo = %s", param_list)
        c.miConexion.commit()
        miCursor.close()

    def restar(self, id_prestamo, cantidad):
        c = Conexion.Conexion()
        miCursor = c.miConexion.cursor()
        param_list = [cantidad, id_prestamo]
        miCursor.execute("Update prestamo   Set cantidad = cantidad - %s  where id_prestamo = %s", param_list)
        c.miConexion.commit()
        miCursor.close()

    def eliminar(self, id_prestamo):
        c = Conexion.Conexion()
        miCursor = c.miConexion.cursor()
        param_list = [id_prestamo]
        miCursor.execute("Delete FROM public.prestamo WHERE id_prestamo = %s", param_list)
        c.miConexion.commit()
        miCursor.close()

    def insertar(self, desde , para, cantidad):
        c = Conexion.Conexion()
        miCursor = c.miConexion.cursor()
        param_list = [ desde , para, cantidad]
        miCursor.execute("Update prestamo   Set cantidad = cantidad + %s  where id_prestamo = %s", param_list)
        c.miConexion.commit()
        miCursor.close()
    '''


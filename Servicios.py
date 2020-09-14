from Persona import Persona
import sys, psycopg2
import Singleton
import Conexion

@Singleton.SingletonDecorator
class Servicios():
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
		
	def existe_prestamo(self,desde,para):
	    existe = False
	    c = Conexion.Conexion()
        miCursor = c.miConexion.cursor()
        param_list = [desde,para]
        miCursor.execute("SELECT id_prestamo, desde, para, cantidad FROM public.prestamo WHERE desde = %s AND para = %s",param_list)
        tabla = miCursor.fetchall() 
        for row in tabla:
            existe = True
        miCursor.close()
        return existe	
		
	def prestar(self,desde,para,cantidad):
	    c = Conexion.Conexion()
        miCursor = c.miConexion.cursor()
		param_list = [desde,para,cantidad]
     	if self.existe_prestamo(desde,para)
		   miCursor.execute("SELECT id_prestamo, desde, para, cantidad FROM public.prestamo WHERE desde = %s AND para = %s",param_list)   
		

		
	
		
	

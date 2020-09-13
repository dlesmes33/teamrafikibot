from Info_Mensaje import Info_Mensaje
class Registro():
    grupos = []
    def init(self,grupos = []):
        self.grupos = grupos


    def add(self,info):
        gana = False
        id = info.id_chat
        if len(list(filter(lambda n:n == id, self.grupos )))==0:
            self.grupos.append(id)
            gana = True
        return gana




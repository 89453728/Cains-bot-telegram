import time

class User:
    def __init__(self,id,username: str,blanchus: int,pocket: int,banco: int,tipobanco: int, robado: int):
        self.id = id
        self.username = username
        self.blanchus = blanchus
        self.pocket = pocket
        self.banco = banco
        self.tipobanco = tipobanco
        self.robado = robado

    def dep(self,cantidad :int):
        if (self.pocket >= cantidad): 
            cantidadMax = 5000*(self.tipobanco+1)
            if ((cantidadMax - self.banco) >= cantidad):
                # metes algo de lo que tienes en la cartera en el banco
                self.banco += cantidad
                self.pocket -= cantidad
                return cantidad
            else:
                #es demasiado dinero para lo que soporta el banco asi que simplemente llena al maximo el banco
                sobrante = cantidad - self.banco
                self.pocket -= cantidad
                self.pocket += sobrante
                self.banco = 5000*(self.tipobanco+1)
                return sobrante
        else: 
            return -1
    def ret(self,cantidad):
        if (cantidad <= self.banco):
            self.pocket += cantidad
            self.banco -= cantidad
            return cantidad
        else:
            return -1
    def get(self,cantidad):
        self.pocket += cantidad
        self.blanchus += cantidad
        return cantidad
    def give(self,cantidad):
        if(cantidad <= self.pocket):
            self.pocket -= cantidad
            self.blanchus -= cantidad
            return cantidad 
        else:
            return -1
    def cambiardebanco(self,banco):
        cantidadMax = 5000*(self.tipobanco+1)
        if (banco >= self.tipobanco):
            if (self.banco == cantidadMax and self.pocket >= 0.25*(self.tipobanco + 1)*5000):
                self.tipobanco += 1
                self.blanchus -= 0.25*(self.tipobanco + 1)*5000
                self.pocket -= 0.25*(self.tipobanco + 1)*5000
        else: 
            return -1
    def serRobado(self):
        if ((int(time.time()) - self.robado) > 43200): # han pasado 12 horas y puede volver a ser robado
            return 1
        else: # debes dejarlo descansar hasta que pase ese tiempo de seguridad
            return -1

from empleado.class_empleado import Empleado

class Gerente(Empleado):
    def init(self,idEmpleado,idGerente, passwordGerente):
        super().init(idEmpleado)
        self.idGerente = idGerente
        self.passwordGerente = passwordGerente
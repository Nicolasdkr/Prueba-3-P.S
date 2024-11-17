from empleado.class_empleado import Empleado
from departamento.class_proyecto import Proyecto

class RegistroDeTiempo(Empleado,Proyecto):
    def init(self, idRegistro, idEmpleado, idProyecto, fecha, cantidadHorasTrabajadas, descTareasRealizadas):
        super().init(idEmpleado,idProyecto)
        self.idRegistro = idRegistro
        self.fecha = fecha
        self.cantidadHorasTrabajadas = cantidadHorasTrabajadas
        self.descTareasRealizadas = descTareasRealizadas
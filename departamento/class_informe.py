from empleado.class_empleado import Empleado
from departamento.class_proyecto import Proyecto
from departamento.registro_tiempo import RegistroDeTiempo
from departamento.class_departamento import Departamento

class informe(Empleado,Proyecto,Departamento,RegistroDeTiempo):
    def init(self, idInforme,idEmpleado,idProyecto,idDepartamento,idRegistro):
        super().init(idRegistro,idEmpleado,idProyecto,idDepartamento)
        self.idInforme = idInforme
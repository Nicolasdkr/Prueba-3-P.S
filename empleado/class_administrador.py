from empleado.class_empleado import Empleado
from departamento.class_departamento import Departamento
from empleado.class_gerente import Gerente
from datetime import datetime
import pymysql
import bcrypt
import re

class Administrador(Empleado):
    def __init__(self, idEmpleado, idAdministrador, passwordAdministrador):
        super().init(idEmpleado)
        self.idAdministrador = idAdministrador
        self.passwordAdministrador = passwordAdministrador

    def Crear_empleado(self, nombre, direccion, email, telefono, fecha_inicio_contrato, salario,
                       password_empleado):
        # Conexión a la base de datos
        try:
            self.conexion = pymysql.connect(
                host='localhost',
                user='root',
                password='',
                db='prueba'
            )
            self.prueba = self.conexion.cursor()
            print("Conexión a la base de datos correcta")
        except Exception as e:
            print(f"Error de conexión a la base de datos: {e}")
            return

        # Encriptar contraseña
        password_encode = password_empleado.encode()
        salt = bcrypt.gensalt(12)
        password_hash = bcrypt.hashpw(password_encode, salt)

        # Consulta SQL
        cursor = "INSERT INTO empleado (nombre, direccion, email, telefono, fecha_inicio_contrato, salario, password_empleado) VALUES ('{}', '{}', '{}', {}, '{}', {}, '{}')".format(
             nombre, direccion, email, telefono, fecha_inicio_contrato, salario, password_hash.decode()
        )

        print("Creación de empleado completada")

        try:
            self.prueba.execute(cursor)
            self.conexion.commit()
        except Exception as e:
            print("Error al insertar en la base de datos:", e)
            raise
        finally:
            self.conexion.close()


    def Editar_empleado(self, id_empleado, nuevo_nombre, nueva_direccion, nuevo_email, nuevo_telefono,
                            nueva_fecha_inicio_contrato, nuevo_salario, nuevo_password):
        # Establecer conexión a la base de datos
        try:
            self.conexion = pymysql.connect(
                host='localhost',
                user='root',
                password='',
                db='prueba'
            )
            self.prueba = self.conexion.cursor()
            print("Conexión a la base de datos correcta.")
        except Exception as e:
            print(f"Error de conexión a la base de datos: {e}")
            return

        # Verificar que el ID del empleado es válido
        try:
            self.id_empleado = int(id_empleado)
        except ValueError:
            print("ID inválido, debe ser un número entero.")
            self.conexion.close()
            return

        # Verificar si el empleado existe
        consulta = "SELECT * FROM empleado WHERE id_empleado = {}".format(self.id_empleado)
        self.prueba.execute(consulta)
        resultado = self.prueba.fetchone()

        if not resultado:
            print(f"No existe un empleado con id_empleado={self.id_empleado}")
            self.conexion.close()
            return

        # Encriptar la nueva contraseña
        if nuevo_password:
            password_encode = nuevo_password.encode()
            salt = bcrypt.gensalt(12)
            password_hash = bcrypt.hashpw(password_encode, salt).decode()
        else:
            # Si no se proporciona nueva contraseña, mantener la contraseña actual
            password_hash = resultado[7]  # Asumiendo que la contraseña está en la posición 7

        # Preparar la consulta para actualizar los datos del empleado utilizando .format()
        actualizar = """
                       UPDATE empleado 
                       SET nombre = '{}', direccion = '{}', email = '{}', telefono = '{}', 
                           fecha_inicio_contrato = '{}', salario = {}, password_empleado = '{}'
                       WHERE id_empleado = {}
                   """.format(nuevo_nombre, nueva_direccion, nuevo_email, nuevo_telefono,
                              nueva_fecha_inicio_contrato, nuevo_salario, password_hash, self.id_empleado)

        # Ejecutar la consulta para actualizar los datos
        try:
            self.prueba.execute(actualizar)
            self.conexion.commit()
            print("Actualización completada con éxito.")
        except Exception as e:
            print(f"Error al actualizar los datos del empleado: {e}")
        finally:
            self.conexion.close()


    def Eliminar_empleado(self, id_empleado):
        try:
            self.conexion = pymysql.connect(
                host='localhost',
                user='root',
                password='',
                db='prueba'
            )
            self.prueba = self.conexion.cursor()
        except Exception as e:
            print(f"Error de conexión a la base de datos: {e}")
            return


        consulta = "SELECT * FROM empleado WHERE id_empleado ={}".format(id_empleado)
        self.prueba.execute(consulta)
        resultado = self.prueba.fetchone()


        try:

            if resultado:

                eliminar = """DELETE FROM empleado WHERE id_empleado= {}""".format(id_empleado)

                self.prueba.execute(eliminar)
                self.conexion.commit()
                print("Empleado eliminado")
            else:
                print(f"No existe un empleado con id_empleado={id_empleado}")

        except Exception as e:
            print(f"Error al eliminar: {e}")
            raise
        finally:
            self.conexion.close()

#--------------------------------- PARTE DEPARTAMENTO --------------------------------------------------

    def Crear_departamento(self, password_departamento, id_gerente, id_administrador):
        try:
            # Conexión a la base de datos
            self.conexion = pymysql.connect(
                host='localhost',
                user='root',
                password='',
                db='prueba'
            )
            self.prueba = self.conexion.cursor()
            print("Conexión a la base de datos correcta")
        except Exception as e:
            print(f"Error de conexión a la base de datos: {e}")
            return

        # Validar la longitud de la contraseña
        if len(password_departamento) < 6:
            print("La contraseña debe tener al menos 6 caracteres.")
            return

        # Encriptar la contraseña
        password_encode = password_departamento.encode()
        salt = bcrypt.gensalt(12)
        password_hash = bcrypt.hashpw(password_encode, salt).decode()

        try:
            # Insertar datos en la tabla departamento con una consulta parametrizada
            query = """
                INSERT INTO departamento (password_depto, id_gerente, id_admin) 
                VALUES (%s, %s, %s)
            """
            self.prueba.execute(query, (password_hash, id_gerente, id_administrador))
            self.conexion.commit()
            print("Departamento creado exitosamente.")
        except Exception as e:
            print(f"Error al crear el departamento: {e}")
        finally:
            self.conexion.close()

    def Editar_departamento(self, id_departamento, nuevo_password_departamento, id_gerente, id_administrador):
        try:
            self.conexion = pymysql.connect(
                host='localhost',
                user='root',
                password='',
                db='prueba'
            )
            self.prueba = self.conexion.cursor()
            print("Conexión a la base de datos correcta.")
        except Exception as e:
            print(f"Error de conexión a la base de datos: {e}")
            return

        # Verificar si el departamento existe
        consulta = "SELECT * FROM departamento WHERE id_departamento = %s"
        self.prueba.execute(consulta, (id_departamento,))
        resultado = self.prueba.fetchone()

        if not resultado:
            print(f"No existe un departamento con id_departamento={id_departamento}")
            self.conexion.close()
            return

        # Encriptar la nueva contraseña
        password_encode = nuevo_password_departamento.encode()
        salt = bcrypt.gensalt(12)
        password_hash = bcrypt.hashpw(password_encode, salt).decode()

        # Consulta de actualización usando placeholders
        actualizar = """
                   UPDATE departamento 
                   SET password_depto = %s, id_gerente = %s, id_admin = %s
                   WHERE id_departamento = %s
               """

        # Ejecutar la consulta de actualización
        try:
            self.prueba.execute(actualizar, (password_hash, id_gerente, id_administrador, id_departamento))
            self.conexion.commit()
            print("Actualización del departamento completada.")
        except Exception as e:
            print(f"Error al actualizar el departamento: {e}")
        finally:
            self.conexion.close()

    def Eliminar_departamento(self, id_departamento):
        try:
            self.conexion = pymysql.connect(
                host='localhost',
                user='root',
                password='',
                db='prueba'
            )
            self.prueba = self.conexion.cursor()
        except Exception as e:
            print(f"Error de conexión a la base de datos: {e}")
            return

        consulta = "SELECT * FROM departamento WHERE id_departamento ={}".format(id_departamento)
        self.prueba.execute(consulta)
        resultado = self.prueba.fetchone()

        try:

            if resultado:

                eliminar = """DELETE FROM departamento WHERE id_departamento= {}""".format(id_departamento)

                self.prueba.execute(eliminar)
                self.conexion.commit()
                print("Empleado eliminado")
            else:
                print(f"No existe un empleado con id_empleado={id_departamento}")

        except Exception as e:
            print(f"Error al eliminar: {e}")
            raise
        finally:
            self.conexion.close()






        self.conexion.close()

    # --------------------------------- PARTE GERENTE --------------------------------------------------

    def Crear_Gerente(self, id_empleado, password_gerente):
        try:
            self.conexion = pymysql.connect(
                host='localhost',
                user='root',
                password='',
                db='prueba'
            )
            self.prueba = self.conexion.cursor()
            print("Conexion bd correcta")
        except Exception as e:
            print(f"Error de conexión a la base de datos: {e}")
            return

        password_encode = password_gerente.encode()
        salt = bcrypt.gensalt(12)
        password_hash = bcrypt.hashpw(password_encode, salt)

        cursor = "INSERT into gerente (id_empleado, password_gerente) values ({},'{}')".format(id_empleado,
                                                                                               password_hash.decode())

        print("Creación de gerente completada")

        try:
            self.prueba.execute(cursor)
            self.conexion.commit()
        except Exception as e:
            print("El valor ya existe", e)
            raise
        finally:
            self.conexion.close()

    def Validar_admin(self, id_admin, password_admin):
        try:
            self.conexion = pymysql.connect(
                host='localhost',
                user='root',
                password='',
                db='prueba'
            )
            self.prueba = self.conexion.cursor()
            print("Conexión a la base de datos correcta")

            # Usar marcadores de posición para evitar inyección SQL
            consulta = "SELECT * FROM administrador WHERE id_administrador = %s AND password_admin = %s"

            # Ejecutar la consulta con los valores proporcionados
            self.prueba.execute(consulta, (id_admin, password_admin))

            # Verificar si la consulta devolvió algún resultado
            resultado = self.prueba.fetchone()

            if resultado:
                print("Admin válido")
                return True
            else:
                print("ID o contraseña incorrectos")
                return False

        except Exception as e:
            print(f"Error de conexión a la base de datos: {e}")
            return False

        finally:
            # Cerrar la conexión a la base de datos
            if self.conexion:
                self.conexion.close()
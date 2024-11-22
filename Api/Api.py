from http.client import responses

import requests
import json
import pymysql


#url = "https://mindicador.cl/api"

#response = requests.get(url)
#data = json.loads(response.text.encode("utf-8"))
#pretty_json = json.dumps(data, indent=2)
#print(pretty_json)


class Dinero():


    def divisaFunction(self,divisa,fecha):
        url = f"https://mindicador.cl/api/{divisa}/{fecha}"

        response = requests.get(url)
        datafecha = response.json()
        valor = None
        pretty_json = json.dumps(datafecha, indent=2)
        print(pretty_json)

        try:
            valor = datafecha["serie"][0]["valor"]
        except(KeyError, IndexError):
            valor = None
            return valor

        if divisa == "ipc":
            porcentaje = valor
            valor = '{}%'.format(porcentaje)

        print(valor)

        return valor

    def subirABD(self, divisa, fecha, valor, rut, fecha_actual):
        # Conexión a la base de datos
        try:
            self.conexion = pymysql.connect(
                host='localhost',
                user='root',
                password='',
                db='prueba2'
            )
            self.prueba = self.conexion.cursor()
            print("Conexión a la base de datos correcta")
        except Exception as e:
            print(f"Error de conexión a la base de datos: {e}")
            return

        url = "https://mindicador.cl"
        fecha_usuario_consulta = 20-11-2024
        id_empleado_registro = "22072608-8"

        # Consulta SQL
        cursor = "INSERT INTO divisa (fecha_usuario_consulta, id_empleado_registro, sitio_info, indicador, fecha_de_Registro, valor_indicador) VALUES ('{}', {}, '{}', '{}', '{}', {})".format(
            fecha_actual,rut, url, divisa, fecha, valor
        )

        print("Creación de registro divisa completado")

        try:
            self.prueba.execute(cursor)
            self.conexion.commit()
        except Exception as e:
            print("Error al insertar en la base de datos:", e)
            raise
        finally:
            self.conexion.close()
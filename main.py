import re
import hashlib
import pymysql
import bcrypt
from empleado.class_administrador import Administrador
from empleado.class_empleado import Empleado
from tkinter import Tk, Label, Button, Entry, Frame, messagebox, mainloop
import mysql.connector
import pymysql
import pymysql
import mysql.connector
from itertools import cycle


# Configuración de la conexión inicial (sin base de datos)
host = 'localhost'
user = 'root'  # Cambia esto por tu usuario de MySQL
password = ''  # Cambia esto por tu contraseña de MySQL
database = 'prueba2'  # Nombre de la base de datos

try:
    # Conexión al servidor MySQL sin base de datos específica
    conexion = mysql.connector.connect(
        host=host,
        user=user,
        password=password
    )
    cursor = conexion.cursor()

    # Verificar si la base de datos ya existe
    cursor.execute("SHOW DATABASES")
    bases_de_datos = [db[0] for db in cursor.fetchall()]

    if database not in bases_de_datos:
        cursor.execute(f"CREATE DATABASE {database}")
        print(f"Base de datos '{database}' creada.")
    else:
        print(f"La base de datos '{database}' ya existe.")

    # Conectar a la base de datos existente o recién creada
    cursor.execute(f"USE {database}")

    # Verificar si las tablas existen antes de crearlas
    cursor.execute("SHOW TABLES")
    tablas_existentes = [tabla[0] for tabla in cursor.fetchall()]

    tablas_a_crear = {
        "departamento": """
            CREATE TABLE departamento (
                id_departamento INT(11) NOT NULL,
                password_depto VARCHAR(10) NOT NULL,
                id_gerente INT(11) NOT NULL,
                id_emp VARCHAR(12) NOT NULL,  -- Se usa VARCHAR para RUT
                id_admin INT(11) NOT NULL,
                PRIMARY KEY (id_departamento)
            )
        """,
        "empleado": """
            CREATE TABLE empleado (
                id_empleado VARCHAR(12) NOT NULL,  -- RUT como clave primaria
                nombre VARCHAR(45) NOT NULL,
                direccion VARCHAR(45) NOT NULL,
                email VARCHAR(45) NOT NULL,
                telefono INT(11) NOT NULL,
                fecha_inicio_contrato VARCHAR(100) NOT NULL,
                salario FLOAT NOT NULL,
                password_empleado VARCHAR(50) NOT NULL,
                PRIMARY KEY (id_empleado)
            )
        """,
        "gerente": """
            CREATE TABLE gerente (
                id_gerente INT(11) NOT NULL,
                password_gerente VARCHAR(10) NOT NULL,
                id_empleado VARCHAR(12) NOT NULL,  -- Vinculado a empleado por RUT
                PRIMARY KEY (id_gerente),
                KEY id_empleado_idx (id_empleado)
            )
        """,
        "informe": """
            CREATE TABLE informe (
                idinforme INT(11) NOT NULL,
                ideempleado VARCHAR(12) NOT NULL,  -- Vinculado a empleado por RUT
                iddepto INT(11) NOT NULL,
                idregistros INT(11) NOT NULL,
                id_proyecto INT(11) NOT NULL,
                PRIMARY KEY (idinforme),
                KEY idempl_idx (ideempleado),
                KEY idproyect_idx (id_proyecto),
                KEY iddepto_idx (iddepto),
                KEY idregistro_idx (idregistros)
            )
        """,
        "proyecto": """
            CREATE TABLE proyecto (
                id_proyecto INT(11) NOT NULL,
                nombre VARCHAR(45) NOT NULL,
                descripcion VARCHAR(45) NOT NULL,
                fecha_inicio INT(11) NOT NULL,
                password_proyecto VARCHAR(10) NOT NULL,
                idemp VARCHAR(12) NOT NULL,  -- Vinculado a empleado por RUT
                PRIMARY KEY (id_proyecto),
                KEY idempl_idx (idemp)
            )
        """,
        "registro_tiempo": """
            CREATE TABLE registro_tiempo (
                id_registro_tiempo INT(11) NOT NULL,
                fecha INT(11) NOT NULL,
                hrs_trabajadas INT(11) NOT NULL,
                desc_tarea VARCHAR(100) NOT NULL,
                idproyecto INT(11) NOT NULL,
                idemp VARCHAR(12) NOT NULL,  -- Vinculado a empleado por RUT
                PRIMARY KEY (id_registro_tiempo),
                KEY ideemp_idx (idemp),
                KEY idproyecto_idx (idproyecto)
            )
        """
    }

    # Crear tablas solo si no existen
    for nombre_tabla, sql_creacion in tablas_a_crear.items():
        if nombre_tabla not in tablas_existentes:
            cursor.execute(sql_creacion)
            print(f"Tabla '{nombre_tabla}' creada.")
        else:
            print(f"La tabla '{nombre_tabla}' ya existe.")

    # Añadir restricciones de clave foránea
    restricciones = [
        "ALTER TABLE gerente ADD CONSTRAINT fk_empleado FOREIGN KEY (id_empleado) REFERENCES empleado (id_empleado)",
        "ALTER TABLE departamento ADD CONSTRAINT fk_idadmin FOREIGN KEY (id_admin) REFERENCES empleado (id_empleado), ADD CONSTRAINT fk_idemp FOREIGN KEY (id_emp) REFERENCES empleado (id_empleado), ADD CONSTRAINT fk_idgerente FOREIGN KEY (id_gerente) REFERENCES gerente (id_gerente)",
        "ALTER TABLE informe ADD CONSTRAINT fk_iddepto FOREIGN KEY (iddepto) REFERENCES departamento (id_departamento), ADD CONSTRAINT fk_idemple FOREIGN KEY (ideempleado) REFERENCES empleado (id_empleado), ADD CONSTRAINT fk_idproyecto FOREIGN KEY (id_proyecto) REFERENCES proyecto (id_proyecto), ADD CONSTRAINT fk_idregistro FOREIGN KEY (idregistros) REFERENCES registro_tiempo (id_registro_tiempo)",
        "ALTER TABLE proyecto ADD CONSTRAINT fk_idempl FOREIGN KEY (idemp) REFERENCES empleado (id_empleado)",
        "ALTER TABLE registro_tiempo ADD CONSTRAINT fk_ideemp FOREIGN KEY (idemp) REFERENCES empleado (id_empleado), ADD CONSTRAINT fk_idproyecto FOREIGN KEY (idproyecto) REFERENCES proyecto (id_proyecto)"
    ]

    for restriccion in restricciones:
        try:
            cursor.execute(restriccion)
        except mysql.connector.Error as err:
            print(f"Error al aplicar la restricción: {err}")

    print("Tablas y restricciones verificadas exitosamente.")

    cursor.close()
    conexion.close()

    # Conexión final con pymysql para realizar operaciones
    connection = pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    print("Conexión exitosa a la base de datos.")

    cursor = connection.cursor()
    cursor.execute("SHOW TABLES")
    for table in cursor.fetchall():
        print(table)

    cursor.close()
    connection.close()

except mysql.connector.Error as e:
    print(f"Error de MySQL: {e}")
except pymysql.MySQLError as e:
    print(f"Error de PyMySQL: {e}")

class Login:
    def __init__(self):
        self.ventana = Tk()
        self.ventana.geometry("400x400")
        self.ventana.title("Login")

        fondo = "#ff6347"

        ##########FRAMES###########

        self.frame_superior = Frame(self.ventana)
        self.frame_superior.configure(bg=fondo)
        self.frame_superior.pack(fill="both", expand=True)

        self.frame_inferior = Frame(self.ventana)
        self.frame_inferior.configure(bg=fondo)
        self.frame_inferior.pack(fill="both", expand=True)

        self.frame_inferior.columnconfigure(0, weight=1)
        self.frame_inferior.columnconfigure(1, weight=1)

        ##########TITULO###########

        self.titulo = Label(self.frame_superior,
                            text="Selección Rol",
                            font=("Tahoma", 36, "bold"),
                            bg=fondo)
        self.titulo.pack(side="top", pady=50)

        #########DATOS##############
        self.botoningresa_empleado = Button(self.frame_inferior,
                                            text="Empleado",
                                            width=100,
                                            font=("Helvetica", 14),
                                            command=self.ingresoemp)
        self.botoningresa_empleado.grid(row=1, column=1, padx=50, pady=5)

        self.botoningresa_Admin = Button(self.frame_inferior,
                                         text="Administrador",
                                         width=100,
                                         font=("Helvetica", 14),
                                         command=self.v_admin)
        self.botoningresa_Admin.grid(row=2, column=1, padx=50, pady=5)

        #####FIN#####
        mainloop()

    def ingresoemp(self):
        self.ventana.destroy()

        self.ventana = Tk()
        self.ventana.geometry("700x700")
        self.ventana.title("aaaa")

        fondo = "#ff6347"

    def v_admin(self):
        self.ventana.destroy()

        self.ventana = Tk()
        self.ventana.geometry("400x300")
        self.ventana.title("Login")

        fondo = "#ff6347"

        ##########FRAMES###########

        self.frame_superior = Frame(self.ventana)
        self.frame_superior.configure(bg=fondo)
        self.frame_superior.pack(fill="both", expand=True)

        self.frame_inferior = Frame(self.ventana)
        self.frame_inferior.configure(bg=fondo)
        self.frame_inferior.pack(fill="both", expand=True)

        self.frame_inferior.columnconfigure(0, weight=1)
        self.frame_inferior.columnconfigure(1, weight=1)

        ##########TITULO###########

        self.titulo = Label(self.frame_superior,
                            text="Inicio Sesión Admin",
                            font=("Tahoma", 25, "bold"),
                            bg=fondo)
        self.titulo.pack(side="top", pady=40)

        self.label_usuario = Label(self.frame_inferior,
                                   text="id?",
                                   font=("Helvetica", 18),
                                   bg=fondo,
                                   fg="black")
        self.label_usuario.grid(row=0, column=0, padx=10, sticky="e")
        self.entry_usuario = Entry(self.frame_inferior,
                                   bd=0,
                                   width=14,
                                   font=("Helvetica", 18))
        self.entry_usuario.grid(row=0, column=1, columnspan=3, padx=5, sticky="w")

        self.label_contraseña = Label(self.frame_inferior,
                                      text="Contraseña",
                                      font=("Helvetica", 18),
                                      bg=fondo,
                                      fg="black")
        self.label_contraseña.grid(row=1, column=0, padx=10, sticky="e")
        self.entry_contraseña = Entry(self.frame_inferior,
                                      bd=0,
                                      width=14,
                                      font=("Helvetica", 18),
                                      show="ඞ")
        #●
        self.entry_contraseña.grid(row=1, column=1, columnspan=3, padx=5, sticky="w")

        self.boton_ingresar = Button(self.frame_inferior,
                                     text="Ingresar",
                                     width=16,
                                     font=("Helvetica", 12),
                                     command=self.entrar)
        self.boton_ingresar.grid(row=2, column=1, pady=35)

        #Validar Datos administrador

    def entrar(self):
        nombre = self.entry_usuario.get()
        contra = self.entry_contraseña.get()

        if nombre == "1" and contra == "1":
            messagebox.showinfo("Acceso Correcto ", "¡Has iniciado correctamente!")
            self.ventana.destroy()
            self.ventana2()
        else:
            messagebox.showinfo("Acceso Denegado ", " Intentelo Nuevamente")


    ###VENTANA2###

    def ventana2(self):
        self.ventana2 = Tk()
        self.ventana2.geometry("500x600")
        self.ventana2.title("Admin")

        fondo1 = "#ff6347"

        self.frame_superior = Frame(self.ventana2)
        self.frame_superior.configure(bg=fondo1)
        self.frame_superior.pack(fill="both", expand=True)

        self.frame_inferior = Frame(self.ventana2)
        self.frame_inferior.configure(bg=fondo1)
        self.frame_inferior.pack(fill="both", expand=True)

        self.frame_inferior.columnconfigure(0, weight=1)
        self.frame_inferior.columnconfigure(1, weight=1)

        self.titulo2 = Label(self.frame_superior,
                             text="Panel administrador",
                             font=("Tahoma", 30, "bold"),
                             bg=fondo1)
        self.titulo2.pack(side="top", pady=20)

        self.boton_a_empleado = Button(self.frame_inferior,
                                       text="Crear Empleado",
                                       width=100,
                                       font=("Helvetica", 14),
                                       command=self.v_c_emp)
        self.boton_a_empleado.grid(row=1, column=1, padx=50, pady=0)

        self.boton_e_empleado = Button(self.frame_inferior,
                                       text="Editar Empleado",
                                       width=100,
                                       font=("Helvetica", 14),
                                       command=self.v_e_emp)
        self.boton_e_empleado.grid(row=2, column=1, padx=50, pady=10)

        self.boton_d_empleado = Button(self.frame_inferior,
                                       text="Eliminar Empleado",
                                       width=100,
                                       font=("Helvetica", 14),
                                       command=self.v_d_emp)
        self.boton_d_empleado.grid(row=3, column=1, padx=50, pady=0)

        self.boton_c_depa = Button(self.frame_inferior,
                                   text="Crear Departamento ",
                                   width=100,
                                   font=("Helvetica", 14),
                                   command=self.v_c_d)
        self.boton_c_depa.grid(row=4, column=1, padx=50, pady=10)

        self.boton_e_depa = Button(self.frame_inferior,
                                   text="Editar Departamento ",
                                   width=100,
                                   font=("Helvetica", 14),
                                   command=self.v_e_d)
        self.boton_e_depa.grid(row=5, column=1, padx=50, pady=0)

        self.boton_d_depa = Button(self.frame_inferior,
                                   text="Eliminar Departamento ",
                                   width=100,
                                   font=("Helvetica", 14),
                                   command=self.v_d_d)
        self.boton_d_depa.grid(row=6, column=1, padx=50, pady=10)

        self.boton_c_ger = Button(self.frame_inferior,
                                  text="Crear Gerente ",
                                  width=100,
                                  font=("Helvetica", 14),
                                  command=self.v_c_g)
        self.boton_c_ger.grid(row=7, column=1, padx=50, pady=0)


        self.boton_c_div = Button(self.frame_inferior,
                                  text="divisa se me olvideo el nombre ",
                                  width=100,
                                  font=("Helvetica", 14),
                                  command=self.divisa)
        self.boton_c_div.grid(row=8, column=1, padx=50, pady=10)



    ########VENTANA CREAR EMPLEADO##########

    def v_c_emp(self):
        self.v_c_emp = Tk()
        self.v_c_emp.geometry("700x500")
        self.v_c_emp.title("Crear Empleado")

        fondo3 = "#ff6347"

        self.frame_superior = Frame(self.v_c_emp)
        self.frame_superior.configure(bg=fondo3)
        self.frame_superior.pack(fill="both", expand=True)

        self.frame_inferior = Frame(self.v_c_emp)
        self.frame_inferior.configure(bg=fondo3)
        self.frame_inferior.pack(fill="both", expand=True)

        self.frame_inferior.columnconfigure(0, weight=1)
        self.frame_inferior.columnconfigure(1, weight=1)

        self.titulo_c_emp = Label(self.frame_superior,
                                  text="Crear Empleado",
                                  font=("Tahoma", 30, "bold"),
                                  bg=fondo3)
        self.titulo_c_emp.pack(side="top", pady=40)

        ##RUT
        self.label_r_emp = Label(self.frame_inferior,
                                 text="RUT",
                                 font=("Helvetica", 18),
                                 bg=fondo3,
                                 fg="black")
        self.label_r_emp.grid(row=0, column=0, padx=10, sticky="e")
        self.entry_r_emp = Entry(self.frame_inferior,
                                 bd=0,
                                 width=28,
                                 font=("Helvetica", 15))
        self.entry_r_emp.grid(row=0, column=1, columnspan=3, padx=5, sticky="w")

        ###NOMBRE###

        self.label_n_emp = Label(self.frame_inferior,
                                 text="Nombre completo",
                                 font=("Helvetica", 18),
                                 bg=fondo3,
                                 fg="black")
        self.label_n_emp.grid(row=1, column=0, padx=10, sticky="e")
        self.entry_n_emp = Entry(self.frame_inferior,
                                 bd=0,
                                 width=28,
                                 font=("Helvetica", 15))
        self.entry_n_emp.grid(row=1, column=1, columnspan=3, padx=5, sticky="w")

        ###DIRECCION###

        self.label_d_emp = Label(self.frame_inferior,
                                 text="Dirección",
                                 font=("Helvetica", 18),
                                 bg=fondo3,
                                 fg="black")
        self.label_d_emp.grid(row=2, column=0, padx=10, sticky="e")
        self.entry_d_emp = Entry(self.frame_inferior,
                                 bd=0,
                                 width=28,
                                 font=("Helvetica", 15))
        self.entry_d_emp.grid(row=2, column=1, columnspan=3, padx=5, sticky="w")

        ###EMAIL###

        self.label_e_emp = Label(self.frame_inferior,
                                 text="Email",
                                 font=("Helvetica", 18),
                                 bg=fondo3,
                                 fg="black")
        self.label_e_emp.grid(row=3, column=0, padx=10, sticky="e")
        self.entry_e_emp = Entry(self.frame_inferior,
                                 bd=0,
                                 width=28,
                                 font=("Helvetica", 15))
        self.entry_e_emp.grid(row=3, column=1, columnspan=3, padx=5, sticky="w")

        ###TELEFONO###

        self.label_t_emp = Label(self.frame_inferior,
                                 text="Telefono (+569)",
                                 font=("Helvetica", 18),
                                 bg=fondo3,
                                 fg="black")
        self.label_t_emp.grid(row=4, column=0, padx=10, sticky="e")
        self.entry_t_emp = Entry(self.frame_inferior,
                                 bd=0,
                                 width=28,
                                 font=("Helvetica", 15))
        self.entry_t_emp.grid(row=4, column=1, columnspan=3, padx=5, sticky="w")

        ###FECHA DE INICIO DE CONTRATO###

        self.label_f_emp = Label(self.frame_inferior,
                                 text="Fecha inicio de contrato",
                                 font=("Helvetica", 18),
                                 bg=fondo3,
                                 fg="black")
        self.label_f_emp.grid(row=5, column=0, padx=10, sticky="e")
        self.entry_f_emp = Entry(self.frame_inferior,
                                 bd=0,
                                 width=28,
                                 font=("Helvetica", 15))
        self.entry_f_emp.grid(row=5, column=1, columnspan=3, padx=5, sticky="w")

        ###SALARIO###

        self.label_s_emp = Label(self.frame_inferior,
                                 text="Salario",
                                 font=("Helvetica", 18),
                                 bg=fondo3,
                                 fg="black")
        self.label_s_emp.grid(row=6, column=0, padx=10, sticky="e")
        self.entry_s_emp = Entry(self.frame_inferior,
                                 bd=0,
                                 width=28,
                                 font=("Helvetica", 15))
        self.entry_s_emp.grid(row=6, column=1, columnspan=3, padx=5, sticky="w")

        ###PASSWORD EMPLEADO###

        self.label_p_emp = Label(self.frame_inferior,
                                 text="Contraseña empleado",
                                 font=("Helvetica", 18),
                                 bg=fondo3,
                                 fg="black")
        self.label_p_emp.grid(row=7, column=0, padx=10, sticky="e")
        self.entry_p_emp = Entry(self.frame_inferior,
                                 bd=0,
                                 width=28,
                                 font=("Helvetica", 15),
                                 show="●")
        self.entry_p_emp.grid(row=7, column=1, columnspan=3, padx=5, sticky="w")

        ###BOTON INGRESAR###

        self.boton_ingresar2 = Button(self.frame_inferior,
                                      text="Ingresar",
                                      width=16,
                                      font=("Helvetica", 12),
                                      command=self.ingresar)
        self.boton_ingresar2.grid(row=9, column=1, pady=15)


    def ingresar(self):

        while True:
            #Validación de rut
            rut = self.entry_r_emp.get()
            # Verificar si el RUT está vacío
            if not rut:
                messagebox.showwarning("Campo Vacío", "El campo de RUT no puede estar vacío.")
                break

            # Verificar el formato del RUT (dígitos, guión, y dígito verificador)
            if not re.match(r'^\d{1,8}-[\dkK]$', rut):
                messagebox.showwarning("Formato Inválido", "El RUT debe tener el formato 12345678-K.")
                break

            # Separar el cuerpo del RUT y el dígito verificador
            cuerpo, dv = rut.split('-')
            dv = dv.upper()  # Convertir el dígito verificador a mayúscula si es necesario

            # Calcular el dígito verificador esperado
            reversed_digits = map(int, reversed(cuerpo))
            factors = cycle(range(2, 8))
            suma = sum(d * f for d, f in zip(reversed_digits, factors))
            dv_calculado = str((-suma) % 11)
            if dv_calculado == '10':
                dv_calculado = 'K'

            # Comparar el dígito verificador ingresado con el calculado
            if dv != dv_calculado:
                messagebox.showwarning("RUT Incorrecto", "El RUT ingresado no es válido.")
                break


            # Validación del nombre
            nombre = self.entry_n_emp.get()
            if not nombre:
                messagebox.showwarning("Campo Vacío", "El campo de nombre no puede estar vacío.")
                break
            elif len(nombre.split()) < 2:
                messagebox.showwarning("Nombre Incompleto", "El campo debe incluir al menos un nombre y un apellido.")
                break

            # Validación de la dirección
            direccion = self.entry_d_emp.get()
            if not direccion:
                messagebox.showwarning("Campo Vacío", "El campo de dirección no puede estar vacío.")
                break
            elif len(direccion) < 5:  # Ajustar la longitud mínima si es necesario
                messagebox.showwarning("Dirección Invalida", "La dirección debe tener al menos 5 caracteres.")
            elif not re.search(r'\d', direccion):  # Verifica si hay al menos un número en la dirección
                messagebox.showwarning("Dirección Inválida", "La dirección debe contener al menos un número.")
                break

            email = self.entry_e_emp.get()
            if not email:
                messagebox.showwarning("Campo Vacío", "El campo de email no puede estar vacío.")
                break
            elif not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):  # Verifica si el email tiene un formato válido
                messagebox.showwarning("Email Inválido", "Por favor ingrese un email válido.")
                break


            telefono = self.entry_t_emp.get()
            if not telefono:
                messagebox.showwarning("Campo Vacío", "El campo de número de celular no puede estar vacío.")
            elif not re.match(r'^\d{8}$', telefono):
                messagebox.showwarning("Número Inválido",
                                       "Por favor ingrese un número de celular chileno válido de 8 dígitos.")
                break


            f_i_emp = self.entry_f_emp.get()
            if not f_i_emp:
                messagebox.showwarning("Campo Vacío", "El campo de la fecha no puede estar vacío.")
                break
            elif not re.match(r'^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/\d{4}$', f_i_emp):
                messagebox.showwarning("Fecha Inválida", "Por favor ingrese una fecha válida en formato DD/MM/AAAA.")
                break

            salario = self.entry_s_emp.get()
            if not salario:
                messagebox.showwarning("Campo Vacío", "El campo de salario no puede estar vacío.")
                break
            try:
                salario_float = float(salario.replace(".", "").replace(",", ""))  # Convertir a número sin separadores
                if salario_float < 500000:
                    messagebox.showwarning("Salario Inválido", "El salario debe ser de al menos 500,000 pesos.")
                    break
                elif salario_float > 50000000:
                    messagebox.showwarning("Salario Inválido", "El salario no puede exceder los 50,000,000 pesos.")
                    break
            except ValueError:
                messagebox.showwarning("Formato Inválido", "Por favor ingrese un salario válido en pesos chilenos.")
                break


            contraseña = self.entry_p_emp.get()
            if len(contraseña) < 5:
                messagebox.showwarning("Contraseña Inválida", "La contraseña debe tener al menos 5 caracteres.")
                return None

            if not re.search(r'[A-Z]', contraseña):
                messagebox.showwarning("Contraseña Inválida",
                                       "La contraseña debe contener al menos una letra mayúscula.")
                return None

            if not re.search(r'\d', contraseña):
                messagebox.showwarning("Contraseña Inválida", "La contraseña debe contener al menos un número.")
                return None
            else:
                contrasena_hash = hashlib.sha256(contraseña.encode()).hexdigest()
                emp = Administrador.Crear_empleado(self, rut, nombre, direccion, email,
                                               telefono, f_i_emp, salario,
                                               contrasena_hash)
                messagebox.showinfo("", "¡Empleado agregado correctamente!")
                self.v_c_emp.destroy()
                return True

        return False


    #######VENTANA EDICION EMPLEADO###########

    def v_e_emp(self):
        self.v_e_emp = Tk()
        self.v_e_emp.geometry("800x500")
        self.v_e_emp.title("Editar Empleado")

        fondo4 = "#ff6347"

        self.frame_superior = Frame(self.v_e_emp)
        self.frame_superior.configure(bg=fondo4)
        self.frame_superior.pack(fill="both", expand=True)

        self.frame_inferior = Frame(self.v_e_emp)
        self.frame_inferior.configure(bg=fondo4)
        self.frame_inferior.pack(fill="both", expand=True)

        self.frame_inferior.columnconfigure(0, weight=1)
        self.frame_inferior.columnconfigure(1, weight=1)

        self.titulo_e_emp = Label(self.frame_superior,
                                  text="Editar Empleado",
                                  font=("Tahoma", 30, "bold"),
                                  bg=fondo4)
        self.titulo_e_emp.pack(side="top", pady=20)

        ###RUT/IDEMPLEADO

        self.label_i_emp = Label(self.frame_inferior,
                                 text="RUT del Empleado (xxxxxxxx-x)",
                                 font=("Helvetica", 18),
                                 bg=fondo4,
                                 fg="black")
        self.label_i_emp.grid(row=0, column=0, padx=10, sticky="e")
        self.entry_i_emp = Entry(self.frame_inferior,
                                 bd=0,
                                 width=28,
                                 font=("Helvetica", 18))
        self.entry_i_emp.grid(row=0, column=1, columnspan=3, padx=5, sticky="w")

        ###NOMBRE###

        self.label_n_emp = Label(self.frame_inferior,
                                 text="Nombre del Empleado",
                                 font=("Helvetica", 18),
                                 bg=fondo4,
                                 fg="black")
        self.label_n_emp.grid(row=1, column=0, padx=10, sticky="e")
        self.entry_n_emp = Entry(self.frame_inferior,
                                 bd=0,
                                 width=28,
                                 font=("Helvetica", 18))
        self.entry_n_emp.grid(row=1, column=1, columnspan=3, padx=5, sticky="w")

        ###DIRECCION###

        self.label_d_emp = Label(self.frame_inferior,
                                 text="Direccion del Empleado",
                                 font=("Helvetica", 18),
                                 bg=fondo4,
                                 fg="black")
        self.label_d_emp.grid(row=2, column=0, padx=10, sticky="e")
        self.entry_d_emp = Entry(self.frame_inferior,
                                 bd=0,
                                 width=28,
                                 font=("Helvetica", 18))
        self.entry_d_emp.grid(row=2, column=1, columnspan=3, padx=5, sticky="w")

        ###EMAIL###

        self.label_e_emp = Label(self.frame_inferior,
                                 text="Email del Empleado",
                                 font=("Helvetica", 18),
                                 bg=fondo4,
                                 fg="black")
        self.label_e_emp.grid(row=3, column=0, padx=10, sticky="e")
        self.entry_e_emp = Entry(self.frame_inferior,
                                 bd=0,
                                 width=28,
                                 font=("Helvetica", 18))
        self.entry_e_emp.grid(row=3, column=1, columnspan=3, padx=5, sticky="w")

        ###TELEFONO###

        self.label_t_emp = Label(self.frame_inferior,
                                 text="Telefono (+569)",
                                 font=("Helvetica", 18),
                                 bg=fondo4,
                                 fg="black")
        self.label_t_emp.grid(row=4, column=0, padx=10, sticky="e")
        self.entry_t_emp = Entry(self.frame_inferior,
                                 bd=0,
                                 width=28,
                                 font=("Helvetica", 18))
        self.entry_t_emp.grid(row=4, column=1, columnspan=3, padx=5, sticky="w")

        ###FECHA DE INICIO DE CONTRATO###

        self.label_f_emp = Label(self.frame_inferior,
                                 text="Fecha inicio de contrato",
                                 font=("Helvetica", 18),
                                 bg=fondo4,
                                 fg="black")
        self.label_f_emp.grid(row=5, column=0, padx=10, sticky="e")
        self.entry_f_emp = Entry(self.frame_inferior,
                                 bd=0,
                                 width=28,
                                 font=("Helvetica", 18))
        self.entry_f_emp.grid(row=5, column=1, columnspan=3, padx=5, sticky="w")

        ###SALARIO###

        self.label_s_emp = Label(self.frame_inferior,
                                 text="Salario del Empleado",
                                 font=("Helvetica", 18),
                                 bg=fondo4,
                                 fg="black")
        self.label_s_emp.grid(row=6, column=0, padx=10, sticky="e")
        self.entry_s_emp = Entry(self.frame_inferior,
                                 bd=0,
                                 width=28,
                                 font=("Helvetica", 18))
        self.entry_s_emp.grid(row=6, column=1, columnspan=3, padx=5, sticky="w")

        ###PASSWORD EMPLEADO###

        self.label_p_emp = Label(self.frame_inferior,
                                 text="Nueva Contraseña del Empleado",
                                 font=("Helvetica", 18),
                                 bg=fondo4,
                                 fg="black")
        self.label_p_emp.grid(row=7, column=0, padx=10, sticky="e")
        self.entry_p_emp = Entry(self.frame_inferior,
                                 bd=0,
                                 width=28,
                                 font=("Helvetica", 18),
                                 show="●")
        self.entry_p_emp.grid(row=7, column=1, columnspan=3, padx=5, sticky="w")

        ###BOTON INGRESAR###

        self.boton_ingresar3 = Button(self.frame_inferior,
                                      text="Ingresar",
                                      width=16,
                                      font=("Helvetica", 12),
                                      command=self.ingresar2)
        self.boton_ingresar3.grid(row=8, column=1, pady=35)

    def ingresar2(self):
        while True:
            rut = self.entry_i_emp.get()
            nombre = self.entry_n_emp.get()
            direccion = self.entry_d_emp.get()
            email = self.entry_e_emp.get()
            telefono = self.entry_t_emp.get()
            f_i_emp = self.entry_f_emp.get()
            salario = self.entry_s_emp.get()
            contraseña = self.entry_p_emp.get()

            if not rut:
                messagebox.showwarning("Campo Vacío", "El campo de RUT no puede estar vacío.")
                break

            # Verificar el formato del RUT (dígitos, guión, y dígito verificador)
            if not re.match(r'^\d{1,8}-[\dkK]$', rut):
                messagebox.showwarning("Formato Inválido", "El RUT debe tener el formato 12345678-K.")
                break

            try:
                conexion = pymysql.connect(
                    host='localhost',
                    user='root',
                    password='',
                    db='prueba2'
                )
                cursor = conexion.cursor()
                consulta = "SELECT id_empleado FROM empleado WHERE id_empleado = %s"
                cursor.execute(consulta, (rut,))
                resultado = cursor.fetchone()

                if not resultado:
                    messagebox.showwarning("RUT No Encontrado", f"No existe un empleado con el RUT: {rut}.")
                    conexion.close()
                    break
                conexion.close()
            except Exception as e:
                messagebox.showerror("Error", f"Error al verificar el RUT: {e}")
                break

            if not nombre:
                messagebox.showwarning("Campo Vacío", "El campo de nombre no puede estar vacío.")
                break
            elif len(nombre.split()) < 2:
                messagebox.showwarning("Nombre Incompleto", "El campo debe incluir al menos un nombre y un apellido.")
                break

            if not direccion:
                messagebox.showwarning("Campo Vacío", "El campo de dirección no puede estar vacío.")
                break
            elif len(direccion) < 5:  # Ajustar la longitud mínima si es necesario
                messagebox.showwarning("Dirección Invalida", "La dirección debe tener al menos 5 caracteres.")
            elif not re.search(r'\d', direccion):  # Verifica si hay al menos un número en la dirección
                messagebox.showwarning("Dirección Inválida", "La dirección debe contener al menos un número.")
                break

            if not telefono:
                messagebox.showwarning("Campo Vacío", "El campo de número de celular no puede estar vacío.")
            elif not re.match(r'^\d{8}$', telefono):
                messagebox.showwarning("Número Inválido",
                                       "Por favor ingrese un número de celular chileno válido de 8 dígitos.")
                break

            if not f_i_emp:
                messagebox.showwarning("Campo Vacío", "El campo de la fecha no puede estar vacío.")
                break
            elif not re.match(r'^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/\d{4}$', f_i_emp):
                messagebox.showwarning("Fecha Inválida", "Por favor ingrese una fecha válida en formato DD/MM/AAAA.")
                break

            if not salario:
                messagebox.showwarning("Campo Vacío", "El campo de salario no puede estar vacío.")
                break
            try:
                salario_float = float(salario.replace(".", "").replace(",", ""))  # Convertir a número sin separadores
                if salario_float < 500000:
                    messagebox.showwarning("Salario Inválido", "El salario debe ser de al menos 500,000 pesos.")
                    break
                elif salario_float > 50000000:
                    messagebox.showwarning("Salario Inválido", "El salario no puede exceder los 50,000,000 pesos.")
                    break
            except ValueError:
                messagebox.showwarning("Formato Inválido", "Por favor ingrese un salario válido en pesos chilenos.")
                break


            # Validar la contraseña
            if len(contraseña) < 5 or not re.search(r'[A-Z]', contraseña) or not re.search(r'\d', contraseña):
                messagebox.showwarning("Contraseña Inválida",
                                       "Debe tener al menos 5 caracteres, una mayúscula y un número.")
                break

            # Encriptar la contraseña
            contrasena_hash = hashlib.sha256(contraseña.encode()).hexdigest()

            # Llamar al método de actualización
            emp = Administrador.Editar_empleado(self, rut, nombre, direccion, email,
                                               telefono, f_i_emp, salario,
                                               contraseña)
            # Confirmar y cerrar
            messagebox.showinfo("", "¡Empleado editado correctamente!")
            self.v_e_emp.destroy()
            return True

        return False

    ########VENTANA ELIMINAR EMPLEADO##########################
    def v_d_emp(self):
        self.v_d_emp = Tk()
        self.v_d_emp.geometry("500x400")
        self.v_d_emp.title("Eliminar Empleado")

        fondo4 = "#ff6347"

        self.frame_superior = Frame(self.v_d_emp)
        self.frame_superior.configure(bg=fondo4)
        self.frame_superior.pack(fill="both", expand=True)

        self.frame_inferior = Frame(self.v_d_emp)
        self.frame_inferior.configure(bg=fondo4)
        self.frame_inferior.pack(fill="both", expand=True)

        self.frame_inferior.columnconfigure(0, weight=1)
        self.frame_inferior.columnconfigure(1, weight=1)

        self.titulo_e_emp = Label(self.frame_superior,
                                  text="Eliminar Empleado",
                                  font=("Calisto MT", 36, "bold"),
                                  bg=fondo4)
        self.titulo_e_emp.pack(side="top", pady=20)

        ###IDEMPLEADO###

        self.label_i_emp = Label(self.frame_inferior,
                                 text="Id Empleado",
                                 font=("Arial", 18),
                                 bg=fondo4,
                                 fg="black")
        self.label_i_emp.grid(row=0, column=0, padx=10, sticky="e")
        self.entry_i_emp = Entry(self.frame_inferior,
                                 bd=0,
                                 width=14,
                                 font=("Arial", 18))
        self.entry_i_emp.grid(row=0, column=1, columnspan=3, padx=5, sticky="w")

        self.boton_eliminar = Button(self.frame_inferior,
                                     text="Eliminar",
                                     width=16,
                                     font=("Arial", 12),
                                     command=self.eliminar)
        self.boton_eliminar.grid(row=1, column=1, pady=35)

    def eliminar(self):
        id_empleado = self.entry_i_emp.get()  # Suponiendo que el RUT está en esta entrada

        emp = Administrador.Eliminar_empleado(self, id_empleado)  # Llamar a la función Eliminar_empleado

        # Mostrar mensaje de éxito
        messagebox.showinfo("Eliminación", "Empleado eliminado correctamente.")
        self.v_d_emp.destroy()

    ########VENTANA CREAR DEPARTAMENTO########
    def v_c_d(self):
        self.v_c_d = Tk()
        self.v_c_d.geometry("400x700")
        self.v_c_d.title("Crear Departamento")

        fondo4 = "#9fbbf3"

        self.frame_superior = Frame(self.v_c_d)
        self.frame_superior.configure(bg=fondo4)
        self.frame_superior.pack(fill="both", expand=True)

        self.frame_inferior = Frame(self.v_c_d)
        self.frame_inferior.configure(bg=fondo4)
        self.frame_inferior.pack(fill="both", expand=True)

        self.frame_inferior.columnconfigure(0, weight=1)
        self.frame_inferior.columnconfigure(1, weight=1)

        self.titulo_c_d = Label(self.frame_superior,
                                text="Crear Departamento",
                                font=("Calisto MT", 36, "bold"),
                                bg=fondo4)
        self.titulo_c_d.pack(side="top", pady=20)

        ###idsss###
        self.label_g_d = Label(self.frame_inferior,
                               text="ID Gerente",
                               font=("Arial", 18),
                               bg=fondo4,
                               fg="black")
        self.label_g_d.grid(row=1, column=0, padx=10, sticky="e")
        self.entry_g_d = Entry(self.frame_inferior,
                               bd=0,
                               width=14,
                               font=("Arial", 18))
        self.entry_g_d.grid(row=1, column=1, columnspan=3, padx=5, sticky="w")

        self.label_a_d = Label(self.frame_inferior,
                               text="ID Admin",
                               font=("Arial", 18),
                               bg=fondo4,
                               fg="black")
        self.label_a_d.grid(row=3, column=0, padx=10, sticky="e")
        self.entry_a_d = Entry(self.frame_inferior,
                               bd=0,
                               width=14,
                               font=("Arial", 18))
        self.entry_a_d.grid(row=3, column=1, columnspan=3, padx=5, sticky="w")

        self.label_p_d = Label(self.frame_inferior,
                               text="Contraseña Depertamento",
                               font=("Arial", 18),
                               bg=fondo4,
                               fg="black")
        self.label_p_d.grid(row=4, column=0, padx=10, sticky="e")
        self.entry_p_d = Entry(self.frame_inferior,
                               bd=0,
                               width=14,
                               font=("Arial", 18),
                               show="●")
        self.entry_p_d.grid(row=4, column=1, columnspan=3, padx=5, sticky="w")

        self.boton_c_d = Button(self.frame_inferior,
                                text="Crear",
                                width=16,
                                font=("Arial", 12),
                                command=self.creardepto)
        self.boton_c_d.grid(row=5, column=1, pady=35)

    def creardepto(self):
        idgerente = self.entry_g_d.get()
        idadmin = self.entry_a_d.get()
        passdept = self.entry_p_d.get()

        emp = Administrador.Crear_departamento(self, passdept, idgerente, idadmin,)
        ###GUARDAR####

        messagebox.showinfo("", "Departamento Creado correctamente")

        self.v_c_d.destroy()

    def v_e_d(self):
        self.v_e_d = Tk()
        self.v_e_d.geometry("400x700")
        self.v_e_d.title("Editar Departamento")

        fondo4 = "#9fbbf3"

        self.frame_superior = Frame(self.v_e_d)
        self.frame_superior.configure(bg=fondo4)
        self.frame_superior.pack(fill="both", expand=True)

        self.frame_inferior = Frame(self.v_e_d)
        self.frame_inferior.configure(bg=fondo4)
        self.frame_inferior.pack(fill="both", expand=True)

        self.frame_inferior.columnconfigure(0, weight=1)
        self.frame_inferior.columnconfigure(1, weight=1)

        self.titulo_e_d = Label(self.frame_superior,
                                text="Editar Departamento",
                                font=("Calisto MT", 36, "bold"),
                                bg=fondo4)
        self.titulo_e_d.pack(side="top", pady=20)

        self.label_i_d = Label(self.frame_inferior,
                               text="ID Departamento",
                               font=("Arial", 18),
                               bg=fondo4,
                               fg="black")
        self.label_i_d.grid(row=0, column=0, padx=10, sticky="e")
        self.entry_i_d = Entry(self.frame_inferior,
                               bd=0,
                               width=14,
                               font=("Arial", 18))
        self.entry_i_d.grid(row=0, column=1, columnspan=3, padx=5, sticky="w")

        self.label_g_d = Label(self.frame_inferior,
                               text="ID Gerente",
                               font=("Arial", 18),
                               bg=fondo4,
                               fg="black")
        self.label_g_d.grid(row=1, column=0, padx=10, sticky="e")
        self.entry_g_d = Entry(self.frame_inferior,
                               bd=0,
                               width=14,
                               font=("Arial", 18))
        self.entry_g_d.grid(row=1, column=1, columnspan=3, padx=5, sticky="w")


        self.label_a_d = Label(self.frame_inferior,
                               text="ID Admin",
                               font=("Arial", 18),
                               bg=fondo4,
                               fg="black")
        self.label_a_d.grid(row=3, column=0, padx=10, sticky="e")
        self.entry_a_d = Entry(self.frame_inferior,
                               bd=0,
                               width=14,
                               font=("Arial", 18))
        self.entry_a_d.grid(row=3, column=1, columnspan=3, padx=5, sticky="w")

        self.label_p_d = Label(self.frame_inferior,
                               text="Contraseña Depertamento",
                               font=("Arial", 18),
                               bg=fondo4,
                               fg="black")
        self.label_p_d.grid(row=4, column=0, padx=10, sticky="e")
        self.entry_p_d = Entry(self.frame_inferior,
                               bd=0,
                               width=14,
                               font=("Arial", 18),
                               show="●")
        self.entry_p_d.grid(row=4, column=1, columnspan=3, padx=5, sticky="w")

        self.boton_e_d = Button(self.frame_inferior,
                                text="Aceptar",
                                width=16,
                                font=("Arial", 12),
                                command=self.editardepto)
        self.boton_e_d.grid(row=5, column=1, pady=35)


    def editardepto(self):

        iddepto = self.entry_i_d.get()
        passdept = self.entry_p_d.get()
        idgerente = self.entry_g_d.get()
        #idemp = self.entry_i_emp
        idadmin = self.entry_a_d.get()


        emp = Administrador.Editar_departamento(self, iddepto, passdept, idgerente, idadmin)

        messagebox.showinfo("", "Departamento Editado Correctamente")


        self.v_e_d.destroy()


    def v_d_d(self):
        self.v_d_d = Tk()
        self.v_d_d.geometry("400x700")
        self.v_d_d.title("Eliminar Departamento")

        fondo4 = "#9fbbf3"

        self.frame_superior = Frame(self.v_d_d)
        self.frame_superior.configure(bg=fondo4)
        self.frame_superior.pack(fill="both", expand=True)

        self.frame_inferior = Frame(self.v_d_d)
        self.frame_inferior.configure(bg=fondo4)
        self.frame_inferior.pack(fill="both", expand=True)

        self.frame_inferior.columnconfigure(0, weight=1)
        self.frame_inferior.columnconfigure(1, weight=1)

        self.titulo_e_d = Label(self.frame_superior,
                                text="Eliminar Departamento",
                                font=("Calisto MT", 36, "bold"),
                                bg=fondo4)
        self.titulo_e_d.pack(side="top", pady=20)

        self.label_i_d = Label(self.frame_inferior,
                               text="ID Departamento",
                               font=("Arial", 18),
                               bg=fondo4,
                               fg="black")
        self.label_i_d.grid(row=0, column=0, padx=10, sticky="e")
        self.entry_i_d = Entry(self.frame_inferior,
                               bd=0,
                               width=14,
                               font=("Arial", 18))
        self.entry_i_d.grid(row=0, column=1, columnspan=3, padx=5, sticky="w")

        self.boton_eliminar = Button(self.frame_inferior,
                                     text="Eliminar",
                                     width=16,
                                     font=("Arial", 12),
                                     command=self.eliminar2)
        self.boton_eliminar.grid(row=1, column=1, pady=35)


    def eliminar2(self):
        id_depto = self.entry_i_d.get()
        # eliminar#

        emp = Administrador.Eliminar_departamento(self, id_depto)

        messagebox.showinfo("", "Departamento eliminado correctamente")
        self.v_d_d.destroy()


    def v_c_g(self):
        self.v_c_g = Tk()
        self.v_c_g.geometry("400x700")
        self.v_c_g.title("Crear Gerente")

        fondo4 = "#9fbbf3"

        self.frame_superior = Frame(self.v_c_g)
        self.frame_superior.configure(bg=fondo4)
        self.frame_superior.pack(fill="both", expand=True)

        self.frame_inferior = Frame(self.v_c_g)
        self.frame_inferior.configure(bg=fondo4)
        self.frame_inferior.pack(fill="both", expand=True)

        self.frame_inferior.columnconfigure(0, weight=1)
        self.frame_inferior.columnconfigure(1, weight=1)

        self.titulo_c_g = Label(self.frame_superior,
                                text="Crear Gerente",
                                font=("Calisto MT", 36, "bold"),
                                bg=fondo4)
        self.titulo_c_g.pack(side="top", pady=20)

        self.label_c_ig = Label(self.frame_inferior,
                                text="Id Empleado",
                                font=("Arial", 18),
                                bg=fondo4,
                                fg="black")
        self.label_c_ig.grid(row=0, column=0, padx=10, sticky="e")
        self.entry_c_ig = Entry(self.frame_inferior,
                                bd=0,
                                width=14,
                                font=("Arial", 18))
        self.entry_c_ig.grid(row=0, column=1, columnspan=3, padx=5, sticky="w")
        self.label_p_g = Label(self.frame_inferior,
                               text="Contraseña Gerente",
                               font=("Arial", 18),
                               bg=fondo4,
                               fg="black")
        self.label_p_g.grid(row=1, column=0, padx=10, sticky="e")
        self.entry_p_g = Entry(self.frame_inferior,
                               bd=0,
                               width=14,
                               font=("Arial", 18),
                               show="●")
        self.entry_p_g.grid(row=1, column=1, columnspan=3, padx=5, sticky="w")

        self.boton_crear_g = Button(self.frame_inferior,
                                    text="Crear",
                                    width=16,
                                    font=("Arial", 12),
                                    command=self.crear_g)
        self.boton_crear_g.grid(row=2, column=1, pady=35)


    def divisa(self):
        self.divisa = Tk()
        self.divisa.geometry("600x400")
        self.divisa.title("Divisa")

        fondo5 = "#9fbbf3"

        self.frame_superior = Frame(self.divisa)
        self.frame_superior.configure(bg=fondo5)
        self.frame_superior.pack(fill="both", expand=True)

        self.frame_inferior = Frame(self.divisa)
        self.frame_inferior.configure(bg=fondo5)
        self.frame_inferior.pack(fill="both", expand=True)

        self.frame_inferior.columnconfigure(0, weight=1)
        self.frame_inferior.columnconfigure(1, weight=1)

        self.titulo_c_div = Label(self.frame_superior,
                                  text="divisa",
                                  font=("Tahoma", 30, "bold"),
                                  bg=fondo5)
        self.titulo_c_div.pack(side="top", pady=20)

        ###AQUI ESTAN LOS BOTONES TODOS ALUCINES

        self.boton_ingresar3 = Button(self.frame_inferior,
                                      text="divisa",
                                      width=16,
                                      font=("Helvetica", 12),
                                      command=self.ingresar2) #AQUI AGREGAS EL NOMBRE DE LA FUNCION DE LA DIVISA PARA QUE ENTRE
        self.boton_ingresar3.grid(row=1, column=1, pady=35)


        self.boton_ingresar3 = Button(self.frame_inferior,
                                      text="fecha",
                                      width=16,
                                      font=("Helvetica", 12),
                                      command=self.ingresar2)  #AQUI AGREGAS EL NOMBRE DE LA FUNCION DE LA DIVISA
        self.boton_ingresar3.grid(row=0, column=1, pady=35)


#--------------------- AQUI TIENES QUE AGREGAR LAS FUNCIONES O LLAMARLAS, NOSE ESO LO VES TU SKEREEEE

Login()


adm = Administrador()
#adm.Crear_empleado()
#adm.Editar_empleado()
#adm.Eliminar_empleado()
#adm.Crear_departamento()
#adm.Editar_departamento()
#adm.Crear_Gerente()

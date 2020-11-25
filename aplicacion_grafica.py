
from tkinter import ttk 
from tkinter import * 
import os
import sqlite3
import tkinter as tk

class Product:
    db_name = 'database2.db'
    
    def __init__(self, ventana):
        self.ventana_principal = ventana
        #ventana_principal = Tk()
        
        self.ventana_principal.geometry("578x351")
        self.ventana_principal.config(bg = "#C2DC56")
        self.ventana_principal.title("Aplicacion de invernadero")
        Label(self.ventana_principal, text = 'Escoja una opcion').grid(row = 0, rowspan = 3)
        
         
        
        ttk.Button(text = "Acceder", command = self.login ).grid(row = 3, column = 3)
        
        ttk.Button(text = "Registrarse", command = self.registro).grid(row = 3, column = 4)
        ttk.Button(text= "Productos", command = self.productos).grid(row = 3, column = 5)
   
    def productos(self):
        global ventana_producto
        ventana_producto = Toplevel(self.ventana_principal)
        ventana_producto.title("Base de datos de invernadero")
        
        Label(ventana_producto, text = 'Registrar producto').grid(row = 0, column = 0, columnspan = 3, pady = 20)
        #entrada de nombre
        Label(ventana_producto, text = 'Nombre:').grid(row = 1, column = 0)
        self.nombre1 = Entry(ventana_producto)
        self.nombre1.focus()
        self.nombre1.grid(row = 1, column = 1)
        # entrada de precio 
        Label(ventana_producto, text = 'Precio:').grid(row = 2, column = 0)
        self.precio = Entry(ventana_producto)
        self.precio.grid(row = 2, column = 1)
        # boton de añadir producto
        ttk.Button(ventana_producto, text = 'Guardar producto', command = self.add_product).grid(row= 3, columnspan = 2, sticky = W + E)
        # salida de mensajes 
        self.message = Label(ventana_producto, text = '', fg = 'red')
        self.message.grid(row = 6, column = 0, columnspan = 2, sticky = W + E)

        # Tabla 
        self.tree = ttk.Treeview(ventana_producto, height = 10, columns = 2)
        self.tree.grid(row = 4, column = 0, columnspan = 2)
        self.tree.heading('#0', text = 'Nombre', anchor = CENTER)
        self.tree.heading('#1', text = 'Precio', anchor = CENTER)
        ttk.Button(ventana_producto, text = 'Borrar', command = self.delete_product).grid(row = 5, column = 0, sticky =  W + E)
        ttk.Button(ventana_producto, text = 'Editar', command = self.edit_product).grid(row = 5, column = 1, sticky = W + E)

        self.get_products()

    # fucnion de consulta
    def run_query(self, query, parameters = ()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result
        
    # obtener productos de la base 
    def get_products(self):
        # limpiar la tabla
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        # obtener datos
        query = 'SELECT * FROM product ORDER BY nombre1 DESC'
        db_rows = self.run_query(query)
        # llenando datos 
        for row in db_rows:
            self.tree.insert('', 0, text = row [1], values = row[2])
    # validacion de datos
    def validation(self):
        return len(self.nombre1.get()) != 0 and len(self.precio.get()) !=0 # error

    def add_product(self):
        
        if  self.validation():
            query = 'INSERT INTO product VALUES(NULL, ?, ?)'
            parameters = (self.nombre1.get(), self.precio.get())
            self.run_query(query, parameters)
            self.message['text'] = 'Producto agregado {} correctamente'.format(self.nombre1.get())
            self.nombre1.delete(0, END)
            self.precio.delete(0, END)
        else:
            self.message['text'] = 'Nombre y precio requeridos'
        self.get_products()

    def delete_product(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.message['text']= 'Seleciones registro'
            return
        self.message['text'] = ''
        nombre1 = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM product WHERE nombre1 = ?'
        self.run_query(query, (nombre1, ))
        self.message['text'] = 'Registro {} eleminidado con exito'.format(nombre1)
        self.get_products()
    ################################################
    def edit_product(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['values'][0]
        except IndexError as e:
            self.message['text'] = 'Porfavor selecione grabar '
            return
        nombre1 = self.tree.item(self.tree.selection())['text']
        old_price = self.tree.item(self.tree.selection())['values'][0]
        self.edit_wind = Toplevel() #ventana_producto
        self.edit_wind.title = "Editar producto"
        ### Antiguo nombre ####
        Label(self.edit_wind, text = 'Viejo nombre').grid(row = 0, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = nombre1), state = 'readonly').grid(row = 0, column = 2)
        ### Nuevo nombre ###
        Label(self.edit_wind, text = "Nuevo nombre: ").grid(row = 1, column = 1)
        new_name = Entry(self.edit_wind)
        new_name.grid(row = 1, column = 2)

        ### Precio antiguo ###
        Label(self.edit_wind, text = 'Precio antiguo').grid(row = 2, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = old_price), state = 'readonly').grid(row = 2 , column = 2)
        #### Nuevo Precio ### #
        Label(self.edit_wind, text = 'Nuevo precio').grid(row = 3, column = 1)
        new_price = Entry(self.edit_wind)
        new_price.grid(row = 3, column = 2)

        Button(self.edit_wind, text = 'Actualizar', command = lambda: self.edit_records(new_name.get(), nombre1, new_price.get(), old_price)).grid(row = 4, column = 2, sticky = W)
        self.edit_wind.mainloop()

    def edit_records(self, new_name, nombre1, new_price, old_price):
        query = 'UPDATE product SET nombre1 = ?, precio = ? WHERE nombre1 = ? AND precio = ?'
        parameters = (new_name, new_price, nombre1, old_price)
        self.run_query(query, parameters)
        self.edit_wind.destroy()
        self.message['text'] = 'Registro de {} actualizacion con exito'.format(nombre1)
        self.get_products()


    def login(self):
        global ventana_login
        ventana_login = Toplevel(self.ventana_principal)
        ventana_login.title("Acceso a la cuenta")
        ventana_login.geometry("562x281")
        ventana_login.config(bg = "#4B69D7")
        Label(ventana_login, text="Introduzca nombre de usuario y contraseña").grid(row = 2, column = 2, columnspan = 3)
        Label(ventana_login, text="").grid()
        global verifica_usuario
        global verifica_clave
        ##########################3
        verifica_usuario = StringVar()
        verifica_clave = StringVar()
        ##########################
        global entrada_login_usuario 
        global entrada_login_clave
        #########################
        Label(ventana_login, text="Nombre usuario ").grid( column = 1)
        entrada_login_usuario = Entry(ventana_login, textvariable=verifica_usuario)
        entrada_login_usuario.grid(row = 4, column  = 2)
        Label(ventana_login, text="").grid()
        Label(ventana_login, text="Contraseña").grid(column = 1)
        entrada_login_clave = Entry(ventana_login, textvariable=verifica_clave, show='*')
        entrada_login_clave.grid(row = 6 , column = 2)
        Label(ventana_login, text="").grid()
        Button(ventana_login, text="Acceder",  command=self.verifica_login).grid(column = 2)
        #############################################
    
    def registro(self):
        global ventana_registro
        ventana_registro = Toplevel(self.ventana_principal)
        ventana_registro.title("Registro")
        ventana_registro.geometry("400x350")
        global nombre_usuario 
        global clave 
        global entrada_nombre
        global entrada_clave 
        nombre_usuario = StringVar()
        clave = StringVar()
        Label(ventana_registro, text = "Introduzca datos").grid()
        Label(ventana_registro, text="").grid()
        etiqueta_nombre = Label(ventana_registro, text="Nombre de usuario")
        etiqueta_nombre.grid()
        entrada_nombre = Entry(ventana_registro, textvariable = nombre_usuario)
        entrada_nombre.grid()
        etiqueta_clave = Label(ventana_registro, text="Contraseña ")
        etiqueta_clave.grid()
        entrada_clave = Entry(ventana_registro, textvariable=clave, show='*')
        entrada_clave.grid()
        Label(ventana_registro, text="").grid()
        Button(ventana_registro, text="Registrarse", width=10, height=1, command=self.registro_usuario).grid()
    
    def registro_usuario(self):
        usuario_info = nombre_usuario.get()
        clave_info = clave.get()
        file = open(usuario_info, "w")
        file.write(usuario_info + "\n")
        file.write(clave_info)
        file.close()

        entrada_nombre.delete(0, END)
        entrada_clave.delete(0, END)

        Label(ventana_registro, text="Registro completado con éxito", fg="green", font=("calibri", 12)).grid()


    def verifica_login(self):
        usuario1 = verifica_usuario.get()
        clave1 = verifica_clave.get()
        entrada_login_usuario.delete(0, END)
        entrada_login_clave.delete(0,END)
        lista_archivos = os.listdir()
        if usuario1 in lista_archivos:
            archivo1 = open(usuario1, "r")
            verifica = archivo1.read().splitlines()

            ######################
            if clave1 in verifica:
                self.exito_login()
            else:
                self.no_clave()
        else:
            self.no_usuario()
    ###############################        
    def exito_login(self):
        global ventana_exito
        ventana_exito = Toplevel(ventana_login)
        ventana_exito.title("Exito")
        ventana_exito.geometry("300x200")
        Label(ventana_exito, text="Login finalizado con exito").grid()
        Button(ventana_exito, text="OK", command=self.borrar_exito_logn).grid()

    def no_clave(self):
        global ventana_no_clave
        ventana_no_clave = Toplevel(ventana_login)
        ventana_no_clave.title("Error")
        ventana_no_clave.geometry("300x200")
        Label(ventana_no_clave, text="Contraseña incorrecta ").grid()
        Button(ventana_no_clave, text="OK", command=self.borrar_no_clave).grid()
    def no_usuario(self):
        global ventana_no_usuario
        ventana_no_usuario = Toplevel(ventana_login)
        ventana_no_usuario.title("Error")
        ventana_no_usuario.geometry("300x200")
        Label(ventana_no_usuario, text="Usuario no encontrado").grid()
        Button(ventana_no_usuario, Text="OK", command=self.borrar_no_usuario).grid()

    def borrar_exito_logn(self):
        ventana_exito.destroy()
    def borrar_no_clave(self):
        ventana_no_clave.destroy()
    def borrar_no_usuario(self):
        ventana_no_usuario.destroy()









if __name__ == '__main__':
    ventana = Tk()
    application = Product(ventana)
    ventana.mainloop()
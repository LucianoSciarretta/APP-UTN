import sqlite3
from tkinter import ttk, messagebox, Label, Toplevel
from datetime import datetime
import re
import winsound
from peewee import *


db = SqliteDatabase("Trabajo UTN ORM.DB")
# Crea o conecta a la base de datos SQLite
class BaseModel(Model):
    
    class Meta:
        database = db
        

class Items(BaseModel):
    # Definine el modelo de datos para la tabla Items
    #Cuando se instancia la clase Items se genera un nuevo registro en la tabla Items
    
    product_name = CharField(unique = True)
    quantity = CharField()
    price = IntegerField()
    room_name = CharField()
    description = CharField()
    due_date = DateField()
   
#Conexión/Creación de DB
try:
    db.connect()
except OperationalError as error:
    print(f"Error en la creación/conexión de la base de datos: {error}")
except Exception as e:
    print(f"Error general en la creación/conexión con la base de datos: {e}")
   
   
# Intentar crear la tabla Items en la base de datos
try:    
    db.create_tables([Items])
except OperationalError as error:
    print(f"Error en la creación de tablas en la base de datos", error)
except Exception as e:
    print(f"Error general al crear tablas: {e}")
else:
    print("Creación de tablas exitosa")
finally:
    if not db.is_closed():
        db.close()
    

        
class Crud():
    
    """
    Clase que proporciona funciones CRUD para interactuar con la base de datos.
    """
    
    def __init__(self,):
        self.cal_selected = ""
    
    def add(self, product_name, quantity, price, room_name, description, due_date, tree_param, s_option, root):
        
        """
        Agrega un nuevo elemento a la base de datos y actualiza el Treeview.

        :param product_name: Nombre del producto.
        :param quantity: Cantidad del producto.
        :param price: Precio del producto.
        :param room_name: Nombre de la habitación.
        :param description: Descripción del producto.
        :param due_date: Fecha de vencimiento del producto.
        :param tree_param: Objeto Treeview para actualizar.
        :param s_option: Opción de orden para la actualización del Treeview.
        :param root: Ventana principal de la aplicación.
        """
        
        
        item = Items()
        aux = Aux()
        item.product_name = product_name
        item.quantity = quantity
        item.price = price
        item.room_name = room_name
        item.description = description
        item.due_date = due_date
        
        if price <= 0 or quantity <= 0:
             aux.show_message("Error", "El precio y la cantidad \ntienen que ser mayores a cero", root)
             raise Exception("El precio y la cantidad tienen que ser mayores a cero")
     
        try:
            #string a objeto datetime
            item.due_date = datetime.strptime(due_date, "%d/%m/%Y")
            
        except ValueError as error:
         messagebox.showerror(
                "Error",
                "Formato de fecha inválido \nIngrese la fecha en formato DD/MM/AAAA"
         )
         return
        
        if aux.date_validator(due_date):
            item.save()
            self.update_treeview(tree_param, 1)
            self.show_message("Info", "Elemento agregado correctamente", root)
            
        else:
            messagebox.showerror(
                "Error",
                "Formato de fecha inválido \nIngrese la fecha en formato DD/MM/AAAA",
            )
            
    def modify(self, tree_param, var_due_date_param, var_product_name_param, var_quantity_param, var_room_name_param, var_description_param, var_price_param, root, s_option):
        
        """
        Modifica un elemento existente en la base de datos y actualiza el Treeview.

        :param tree_param: Objeto Treeview para actualizar.
        :param var_due_date_param: Variable de control para la fecha de vencimiento.
        :param var_product_name_param: Variable de control para el nombre del producto.
        :param var_quantity_param: Variable de control para la cantidad del producto.
        :param var_room_name_param: Variable de control para el nombre de la habitación.
        :param var_description_param: Variable de control para la descripción del producto.
        :param var_price_param: Variable de control para el precio del producto.
        :param root: Ventana principal de la aplicación.
        :param s_option: Opción de orden para la actualización del Treeview.
        """
        
        
        aux = Aux()
        value = tree_param.selection()
        if not value:
            self.show_message(
                "Info",
                "Por favor, selecione un producto y\nmodifique los campos necesarios",
        root )
        else:
            item_id = tree_param.item(value)["text"]
            
            if aux.date_validator(var_due_date_param.get()):
                due_date = datetime.strptime(var_due_date_param.get(), "%d/%m/%Y")
                data = {
                   'product_name' : var_product_name_param.get(),
                    'quantity' :var_quantity_param.get(),
                    'price' : var_price_param.get(),
                    'room_name' : var_room_name_param.get(),
                    'description' : var_description_param.get(),
                    'due_date' : due_date
                  
                }
                modify =Items.update(data).where(Items.id == item_id)
                modify.execute()
                self.update_treeview(tree_param, s_option)
                self.show_message("Info", "Elemento modificado\ncorrectamente", root)
                self.update_treeview(tree_param, 1)
               
            else:
                messagebox.showerror(
                    "Error",
                    "Formato de fecha inválido \nIngrese la fecha en formato DD/MM/AAAA",
                )

    def delete(self, tree_param, root):
      
        """
        Elimina un elemento de la base de datos y actualiza el Treeview.

        :param tree_param: Elemento del Treeview para actualizar.
        :param root: Ventana principal de la aplicación.
        """
      
        value = tree_param.selection()
        if not value:
            messagebox.showerror(
                "Error", "Por favor, seleccione el item \nque desea eliminar"
            )  
        item = tree_param.item(value)
        delete = Items.get(Items.id == item["text"])
        delete.delete_instance()
        tree_param.delete(value)
        self.show_message("Info", "Elemento eliminado correctamente", root)
        self.update_treeview(tree_param, 1)
        
    def update_treeview(self, my_treeview, s_option):
        
        """
        Actualiza el Treeview con los datos de la base de datos.

        :param my_treeview: Objeto Treeview para actualizar.
        :param s_option: Al elegir un radio button se le asigna un número a esta variable que está asociado a una query específica de tipo SELECT.
        """
        
        items = my_treeview.get_children()
        query = Items.select().order_by(Items.id.asc())
      
        if s_option == 1:
            query = Items.select().order_by(Items.id.asc())
        elif s_option == 2:
            query = Items.select().order_by(Items.price.asc())
        elif s_option == 3:
            query = Items.select().order_by(Items.price.desc())
        elif s_option == 4:
            query = Items.select().order_by(Items.due_date.desc())
                 
        elif self.cal_selected:
            query = query.where(Items.due_date == self.cal_selected)
            
            
        for row in query:
            due_date = row.due_date.strftime('%d/%m/%Y')
            my_treeview.insert(
                "",
                "end",
                text=row.id,
                values=(row.product_name, row.quantity, row.price, row.room_name, row.description, due_date)
            )
        for item in items:
            my_treeview.delete(item)

    def tree_selection(self, product_name, quantity, price, room_name, description, date,  tree_param, event ): 
        
        """
        Actualiza las variables de control con la selección actual del Treeview.

        :param product_name: Variable de control para el nombre del producto.
        :param quantity: Variable de control para la cantidad del producto.
        :param price: Variable de control para el precio del producto.
        :param room_name: Variable de control para el nombre de la habitación.
        :param description: Variable de control para la descripción del producto.
        :param date: Variable de control para la fecha de vencimiento del producto.
        :param tree_param: Objeto Treeview que contiene los datos.
        :param event: Evento de selección en el Treeview.
        """
        
        
        selected_item = tree_param.selection()
        
        if selected_item:
            item_values = tree_param.item(selected_item)["values"]
            product_name.set(item_values[0])
            quantity.set(item_values[1])
            price.set(item_values[2])
            room_name.set(item_values[3])
            description.set(item_values[4])
            date.set(item_values[5])

        ########## CALENDAR SELECTION   ###############

    def cal_selection(self, event, s_option, tree_param, cal_param, root):
        
        self.cal_selected = cal_param.get_date() 
        self.cal_selected = datetime.strptime(self.cal_selected, '%d/%m/%Y')
        self.cal_selected = self.cal_selected.strftime('%Y-%m-%d')
        self.update_treeview(tree_param, self.cal_selected)
        if not tree_param.get_children(): # Si no hay nada en el treeview
            self.show_message("Info", "No se encontraron registros para esta fecha", root)


class Aux:
    
    """
    Clase con funciones auxiliares.
    """
    
    
    
    
    
    def dd_mm_yyyy(self, date):
        """
        Estos métodos los usaba antes PARA formatear fechas de la db al treeview. 
        Ahora lo manejo con los métodos de PEEWEE.
        
        
        english format to spanish format:
        
        """
        en_date = date.split("/")
        en_date[0], en_date[2] = en_date[2], en_date[0]
        spanish_date = "/".join(en_date)
        return spanish_date

        # spanish format to english format:

    def yyyy_mm_dd(self, date):
        sp_date = date.split("/")
        sp_date[0], sp_date[2] = sp_date[2], sp_date[0]
        en_date = "/".join(sp_date)
        return en_date

    def add_slash(self, event, date_entry):
        
        """
        Agrega las  barras automáticamente para respetar el formato de fecha dd/mm/yyyyr.

        :param event: Evento de teclado.
        :param date_entry: Entrada de texto para la fecha.
        """
        
        if len(date_entry.get()) in (2, 5):
            date_entry.insert("end", "/")

    def hover(self, event, color1, color2):
        
        """
        Cambia el color de fondo y el color del texto al pasar el mouse sobre un widget.

        :param event: Evento de movimiento del mouse.
        :param color1: Color de fondo al pasar el mouse.
        :param color2: Color del texto al pasar el mouse.
        """
        
        event.widget.config(bg=color1, fg=color2)

    def leave_hover(self, event,  color1, color2):
        
        """
        Restaura el color de fondo y el color del texto cuando el mouse deja el widget.

        :param event: Evento de salida del mouse.
        :param color1: Color de fondo normal.
        :param color2: Color del texto normal.
        """
        
        event.widget.config(bg=color1, fg=color2)

    def kill_window(self, w):
        
        """
        Cierra una ventana.

        :param w: Ventana a cerrar.
        """
        w.destroy()

    def show_message(self, title, message, root_param):
        """
        Muestra un mensaje emergente.
        Este método lo creé para evitar la molestia de estar cerrando los mensajes emergentes manualmente.
        
        
        :param title: Título del mensaje.
        :param message: Contenido del mensaje.
        :param root_param: Ventana principal de la aplicación.
        """
        
        msg = Toplevel(root_param)
        msg.title(title)

        msg.configure(bg="white", borderwidth=2, relief="groove")
        msg.geometry("300x150")
        msg.resizable(False, False)

        label = Label(msg, text=message, justify="center", padx=10, pady=10)
        label.pack(padx=22, pady=(47, 20))

        screen_width = root_param.winfo_screenwidth()
        screen_height = root_param.winfo_screenheight()

        x = (screen_width - msg.winfo_reqwidth()) // 2
        y = (screen_height - msg.winfo_reqheight()) // 2

        msg.geometry(f"+{x}+{y}")

        root_param.update()
        winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
        msg.after(300, msg.destroy)

    def date_validator(self, due_date):
        
        """
        Valida el formato de fecha con una expresión regular..

        :param due_date: Fecha a validar.
        :return: True si la fecha tiene el formato correcto, False de lo contrario.
        """
        
        
        regular_expression = "\d{2}\/\d{2}\/\d{4}$"
        if re.match(regular_expression, due_date):
            return True
        else:
            return False
                
    def empty_entries(self, *args):
        for arg in args:
            arg.set("")
         
from tkinter import Tk
from view import Window


def main_view(root):
    
    """
    Función principal para iniciar la interfaz gráfica.

    :root: Objeto Tkinter que representa la ventana principal.
    
    
    """
    window = Window(root)


if __name__ == "__main__":
    # Crear una instancia de la ventana principal de la aplicación
    root_tk = Tk()
    main_view(root_tk)
    root_tk.mainloop()

Módulo Main
====================

.. py:function:: main_view(root)

Función principal para iniciar la interfaz gráfica.

Objeto Tkinter que representa la ventana principal.

    

.. code-block:: python

   window = Window(root)


if __name__ == "__main__":

Crea una instancia de la ventana principal de la aplicación

.. code-block:: python

   root_tk = Tk()
   main_view(root_tk)
   root_tk.mainloop()



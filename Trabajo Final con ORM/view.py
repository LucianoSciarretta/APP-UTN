from tkinter import IntVar,  StringVar, DoubleVar, IntVar, ttk, Scrollbar, Frame, Label, Entry, Radiobutton, Button

from model import Crud, Aux
from tkcalendar import Calendar

class Window(Crud, Aux):
    
    """
    Clase que representa la ventana principal de la aplicación.

    Hereda de las clases Crud y Aux para realizar operaciones CRUD y
    utilizar funciones auxiliares.
    """
    
    def __init__(self, root):  
        
        """
        Inicializa la ventana principal.

        :param root: Objeto Tkinter que representa la ventana principal.
        :type root: Tk
        """
        
        super().__init__()
        self.root = root                   
        
        root_color = "#E0FBFC"
        main_color = "#E0FBFC"
        btn_background = "#3D5A80"
        text = "#293241"
        btn_text = "#E0FBFC"
        btn_hover_bg = "#EE6C4D"
        tl_windows = "#98C1D9"
        font1 = "TkMenuFont"
        e_font_size = 13
        radio_font_size = 11
        # MAIN WINDOW

        root.title("Trabajo final")
        root.configure(bg=root_color)

        root.geometry("1000x750+200+10")

        #CAPTURE VARIABLES
        
        var_product_name = StringVar()
        var_quantity = IntVar()
        var_price = DoubleVar()
        var_room_name = StringVar()
        var_description = StringVar()
        var_due_date = StringVar()
        selected_option = IntVar()
        
        ####################### TREEVIEW   #########################################333

        style = ttk.Style()

        style.configure(
            "Treeview.Heading",
            font=("Arial", 12, "bold"),
            background=main_color,
            foreground=text,
        )
        style.configure(
            "Treeview",
            background=btn_background,
            foreground=btn_text,
            rowheight=25,
            font=("Arial", 12),
        )

        self.empty_entries(var_product_name, var_quantity, var_price, var_room_name, var_description, var_due_date)
        tree = ttk.Treeview(root)
        scrollbar = Scrollbar(root, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree["columns"] = ("col1", "col2", "col3", "col4", "col5", "col6")

        tree.column("#0", width=10, anchor="center")
        tree.column("col1", width=40, anchor="w")
        tree.column("col2", width=30, anchor="center")
        tree.column("col3", width=30, anchor="center")
        tree.column("col4", width=50, anchor="center")
        tree.column("col5", width=90, anchor="w")
        tree.column("col6", width=20, anchor="center")

        tree.heading("#0", text="     ID", anchor="center")
        tree.heading("col1", text="PRODUCT NAME")
        tree.heading("col2", text="QUANTITY")
        tree.heading("col3", text="PRICE")
        tree.heading("col4", text="ROOM NAME")
        tree.heading("col5", text="DESCRIPTION")
        tree.heading("col6", text="DUE DATE")

        ############################################

        def change_selected_row_color(event):
            # Función para cambiar el color de la fila seleccionada
            selected_item = tree.selection()
            if selected_item:
                tree.tag_configure("selected", background=btn_hover_bg, foreground=btn_text)
                tree.tag_add("selected", selected_item)

        style.map(
            "Treeview", background=[("selected", btn_hover_bg)], foreground=[("selected", text)]
        )

        tree.pack(fill="x", expand=True, padx=17, pady=(33, 0))
        tree.bind("<<TreeviewSelect>>", lambda event: self.tree_selection( var_product_name,  var_quantity, var_price, var_room_name, var_description,  var_due_date, tree, event))

        # Labels, Entries and Buttons

        frame1 = Frame(root, bg=tl_windows)
        frame1.pack(pady=(0, 22), expand=True, padx=17, ipadx=15)

        product_name_label = Label(
            frame1,
            text="product name: ",
            font=(font1, e_font_size),
            bg=tl_windows,
            fg=text,
        )
        product_name_entry = Entry(
            frame1, textvariable=var_product_name, font=(font1, e_font_size)
        )

        product_name_label.grid(row=0, column=0, sticky="w", ipady=12, padx=12)
        product_name_entry.grid(row=0, column=1)

        quantity_label = Label(
            frame1, text="quantity: ", font=(font1, e_font_size), bg=tl_windows, fg=text
        )
        quantity_entry = Entry(frame1, textvariable=var_quantity, font=(font1, e_font_size))
        quantity_label.grid(row=0, column=2, sticky="w", ipady=12, padx=12)
        quantity_entry.grid(row=0, column=3)

        price_label = Label(
            frame1, text="price: ", font=(font1, e_font_size), bg=tl_windows, fg=text
        )
        price_entry = Entry(frame1, textvariable=var_price, font=(font1, e_font_size))
        price_label.grid(row=0, column=4, sticky="w", ipady=12, padx=12)
        price_entry.grid(row=0, column=5, padx=12)

        room_name_label = Label(
            frame1, text="room name: ", font=(font1, e_font_size), bg=tl_windows, fg=text
        )
        room_name_entry = Entry(frame1, textvariable=var_room_name, font=(font1, e_font_size))
        room_name_label.grid(row=1, column=0, sticky="w", ipady=12, padx=12)
        room_name_entry.grid(row=1, column=1)

        description_label = Label(
            frame1, text="description: ", font=(font1, e_font_size), bg=tl_windows, fg=text
        )
        description_entry = Entry(
            frame1, textvariable=var_description, font=(font1, e_font_size)
        )
        description_label.grid(row=1, column=2, sticky="w", ipady=12, padx=12)
        description_entry.grid(row=1, column=3)

        due_date_label = Label(
            frame1, text="due date: ", font=(font1, e_font_size), bg=tl_windows, fg=text
        )
        due_date_entry = Entry(frame1, textvariable=var_due_date, font=(font1, e_font_size))
        due_date_label.grid(row=1, column=4, sticky="w", ipady=12, padx=12)
        due_date_entry.grid(row=1, column=5)
        due_date_entry.bind("<KeyRelease>", lambda event:self.add_slash(event, due_date_entry))

        #####################    BUTTONS    #############################

        frame2 = Frame(root, bg=tl_windows)
        frame2.pack(side="left", pady=(22, 7), padx=(17, 2))

        frame2_radio = Frame(frame2, bg=tl_windows)
        frame2_radio.pack()

        filters = Label(
            frame2_radio, text="Order by: ", font=(font1, e_font_size), bg=tl_windows, fg=text
        )

        filters.grid(row=0, column=0, sticky="w", padx=7)

        # radio buttons

        all_items = Radiobutton(
            frame2_radio,
            text="All",
            variable=selected_option,
            value=1,
            background=tl_windows,
            fg=text,
            font=(font1, radio_font_size),
            command=lambda: [self.update_treeview(tree, selected_option.get()), self.empty_entries(var_product_name, var_quantity, var_price, var_room_name, var_description, var_due_date)],
        )
        less_price = Radiobutton(
            frame2_radio,
            text="Less price",
            variable=selected_option,
            value=2,
            background=tl_windows,
            fg=text,
            font=(font1, radio_font_size),
            command=lambda: [self.update_treeview(tree, selected_option.get()), self.empty_entries(var_product_name, var_quantity, var_price, var_room_name, var_description, var_due_date)],
        )
        higher_price = Radiobutton(
            frame2_radio,
            text="Higher price",
            variable=selected_option,
            value=3,
            background=tl_windows,
            fg=text,
            font=(font1, radio_font_size),
            command=lambda: [self.update_treeview(tree, selected_option.get()),self.empty_entries(var_product_name, var_quantity, var_price, var_room_name, var_description, var_due_date)],
        )
        by_date = Radiobutton(
            frame2_radio,
            text="Due date",
            variable=selected_option,
            value=4,
            background=tl_windows,
            fg=text,
            font=(font1, radio_font_size),
            command=lambda: [self.update_treeview(tree, selected_option.get()),self.empty_entries(var_product_name, var_quantity, var_price, var_room_name, var_description, var_due_date)],
        )

        all_items.grid(row=0, column=1, pady=12)
        less_price.grid(row=0, column=2, pady=12)
        higher_price.grid(row=0, column=3, pady=12)
        by_date.grid(row=0, column=4, pady=12)

        frame2_btn = Frame(frame2, bg=tl_windows)
        frame2_btn.pack(
            pady=(22, 7),
        )

        btn_submit = Button(
            frame2_btn,
            text="Add",
            font=(font1, e_font_size),
            bg=btn_background,
            fg=btn_text,
            command=lambda : [
                self.add(
                    var_product_name.get(),
                    var_quantity.get(),
                    var_price.get(),
                    var_room_name.get(),
                    var_description.get(),
                    var_due_date.get(),
                    tree, selected_option,
                    root
                ),
                self.empty_entries(var_due_date) if not self.date_validator(var_due_date.get()) else self.empty_entries(var_product_name, var_quantity, var_price, var_room_name, var_description, var_due_date)
            ]
        )
            
        btn_submit.grid(row=0, column=0, sticky="w", pady=12, ipadx=30)
        btn_submit.bind("<Enter>", lambda event:self.hover(event, btn_hover_bg, text))
        btn_submit.bind("<Leave>", lambda event: self.leave_hover( event, btn_background, btn_text))

        btn_modify = Button(
            frame2_btn,
            text="Modify",
            font=(font1, e_font_size),
            bg=btn_background,
            fg=btn_text,
            command=lambda: [self.modify(tree, var_due_date, var_product_name, var_quantity, var_room_name, var_description, var_price, root, selected_option), self.empty_entries(var_due_date) if not self.date_validator(var_due_date.get()) else self.empty_entries(var_product_name, var_quantity, var_price, var_room_name, var_description, var_due_date)],
        )
        btn_modify.grid(row=0, column=1, pady=12, ipadx=22, padx=42)
        btn_modify.bind("<Enter>", lambda event: self.hover(event, btn_hover_bg, text))
        btn_modify.bind("<Leave>", lambda event: self.leave_hover( event, btn_background, btn_text))

        btn_delete = Button(
            frame2_btn,
            text="Delete",
            font=(font1, e_font_size),
            bg=btn_background,
            fg=btn_text,
            command=lambda: [self.delete(tree, root), self.empty_entries(var_due_date) if not self.date_validator(var_due_date.get()) else self.empty_entries(var_product_name, var_quantity, var_price, var_room_name, var_description, var_due_date)]
        )

        btn_delete.grid(row=0, column=2, sticky="e", pady=12, ipadx=22)
        btn_delete.bind("<Enter>", lambda event: self.hover(event, btn_hover_bg, text))
        btn_delete.bind("<Leave>", lambda event: self.leave_hover( event, btn_background, btn_text))
        btn_exit = Button(
            frame2_btn,
            text="Exit",
            font=(font1, e_font_size),
            bg=btn_background,
            fg=btn_text,
            command=lambda: self.kill_window(root),
        )
        btn_exit.grid(row=1, column=0, columnspan=3, ipadx=42, pady=22, ipady=7)
        btn_exit.bind("<Enter>", lambda event: self.hover(event, btn_hover_bg, text))
        btn_exit.bind("<Leave>", lambda event: self.leave_hover( event, btn_background, btn_text))

        ##### CALENDAR #######

        cal_label = Label(
            root,
            text="Select a day in the calendar to see the task",
            background=main_color,
            font=(font1, 17),
            foreground=text,
        )
        cal_label.pack(pady=(0, 12))

        cal = Calendar(root, date_pattern="dd/mm/yyyy")
        cal.configure(
            background=btn_background,
            foreground=btn_text,
            headersbackground=tl_windows,
            headersforeground=text,
        )
        cal.pack(fill="both", expand=True, padx=(7, 17), pady=(7, 17), ipady=29)

        cal.bind("<<CalendarSelected>>", lambda event: self.cal_selection(event, selected_option, tree, cal, root))
        self.update_treeview(tree, selected_option.get())
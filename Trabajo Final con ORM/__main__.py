from tkinter import Tk
from view import Window


def main_view(root):
    window = Window(root)


if __name__ == "__main__":
    root_tk = Tk()
    main_view(root_tk)
    root_tk.mainloop()

import tkinter as tk
from login_window import LoginWindow
from database import initialize_database  # Импортируем функцию

def start_login():
    root = tk.Tk()
    app = LoginWindow(root)
    root.mainloop()

if __name__ == "__main__":
    initialize_database()  # Инициализация базы данных
    start_login()
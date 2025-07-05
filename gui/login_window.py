import tkinter as tk
from tkinter import messagebox
from services.auth_service import autenticar_usuario
from global_state import set_usuario
from gui.main_window import start_main_window
from utils.ui_utils import centrar_ventana

def mostrar_login():
    login = tk.Tk()
    login.title("Login")
    login.geometry("300x200")
    centrar_ventana(login, 300, 200)

    tk.Label(login, text="Email:").pack(pady=5)
    entry_email = tk.Entry(login)
    entry_email.pack()

    tk.Label(login, text="Contraseña:").pack(pady=5)
    entry_password = tk.Entry(login, show="*")
    entry_password.pack()

    def on_login():
        email = entry_email.get()
        password = entry_password.get()

        usuario = autenticar_usuario(email, password)
        if usuario:
            set_usuario(usuario)
            login.destroy()
            start_main_window()
        else:
            messagebox.showerror("Error", "Credenciales inválidas")

    login.bind('<Return>', lambda event: on_login())

    tk.Button(login, text="Iniciar Sesión", command=on_login).pack(pady=20)
    login.mainloop()
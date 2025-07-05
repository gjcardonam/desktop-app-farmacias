import tkinter as tk
from tkinter import messagebox
from services.usuario_service import procesar_nuevo_usuario
from utils.ui_utils import centrar_ventana

def mostrar_formulario_usuario(root):
    ventana = tk.Toplevel(root)
    ventana.title("Agregar Usuario")
    ventana.geometry("400x350")
    centrar_ventana(ventana, 400, 350)

    # Nombre
    tk.Label(ventana, text="Nombre:").pack(pady=5)
    entry_nombre = tk.Entry(ventana)
    entry_nombre.pack()

    # Email
    tk.Label(ventana, text="Email:").pack(pady=5)
    entry_email = tk.Entry(ventana)
    entry_email.pack()

    # Contraseña
    tk.Label(ventana, text="Contraseña:").pack(pady=5)
    entry_password = tk.Entry(ventana, show="*")
    entry_password.pack()

    # Rol
    tk.Label(ventana, text="Rol:").pack(pady=5)
    rol_var = tk.StringVar(ventana)
    rol_var.set("vendedor")  # valor por defecto
    opciones_roles = ["admin", "vendedor"]
    tk.OptionMenu(ventana, rol_var, *opciones_roles).pack()

    # Botón de guardar
    def on_submit():
        nombre = entry_nombre.get()
        email = entry_email.get()
        password = entry_password.get()
        rol = rol_var.get()
        exito, mensaje = procesar_nuevo_usuario(nombre, email, rol, password)
        if exito:
            messagebox.showinfo("Éxito", mensaje)
            ventana.destroy()
        else:
            messagebox.showerror("Error", mensaje)

    tk.Button(ventana, text="Guardar Usuario", command=on_submit).pack(pady=20)
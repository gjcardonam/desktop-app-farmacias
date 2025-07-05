import tkinter as tk
from tkinter import messagebox
from controllers.farmacia_controller import guardar_farmacia
from utils.ui_utils import centrar_ventana

def mostrar_formulario_farmacia(root):
    ventana = tk.Toplevel(root)
    ventana.title("Agregar Farmacia")
    ventana.geometry("400x300")
    centrar_ventana(ventana, 400, 300)

    tk.Label(ventana, text="Nombre:").pack(pady=5)
    entry_nombre = tk.Entry(ventana, width=40)
    entry_nombre.pack()

    tk.Label(ventana, text="NIT:").pack(pady=5)
    entry_nit = tk.Entry(ventana, width=40)
    entry_nit.pack()

    tk.Label(ventana, text="Dirección:").pack(pady=5)
    entry_direccion = tk.Entry(ventana, width=40)
    entry_direccion.pack()

    tk.Label(ventana, text="Teléfono:").pack(pady=5)
    entry_telefono = tk.Entry(ventana, width=40)
    entry_telefono.pack()

    def on_submit():
        nombre = entry_nombre.get()
        nit = entry_nit.get()
        direccion = entry_direccion.get()
        telefono = entry_telefono.get()
        exito, mensaje = guardar_farmacia(nombre, nit, direccion, telefono)
        if exito:
            messagebox.showinfo("Éxito", mensaje)
            ventana.destroy()
        else:
            messagebox.showerror("Error", mensaje)

    tk.Button(ventana, text="Guardar", command=on_submit).pack(pady=20)
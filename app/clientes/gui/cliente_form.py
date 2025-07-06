import tkinter as tk
from tkinter import messagebox
from app.clientes.services.cliente_service import procesar_nuevo_cliente
from utils.ui_utils import centrar_ventana

def mostrar_formulario_cliente(root):
    ventana = tk.Toplevel(root)
    ventana.title("Agregar Cliente")
    ventana.geometry("400x300")
    centrar_ventana(ventana, 400, 300)

    tk.Label(ventana, text="Nombre:").pack(pady=5)
    entry_nombre = tk.Entry(ventana, width=40)
    entry_nombre.pack()

    tk.Label(ventana, text="Documento:").pack(pady=5)
    entry_documento = tk.Entry(ventana, width=40)
    entry_documento.pack()

    tk.Label(ventana, text="Teléfono:").pack(pady=5)
    entry_telefono = tk.Entry(ventana, width=40)
    entry_telefono.pack()

    def on_submit():
        nombre = entry_nombre.get()
        documento = entry_documento.get()
        telefono = entry_telefono.get()
        exito, mensaje = procesar_nuevo_cliente(nombre, documento, telefono)
        if exito:
            messagebox.showinfo("Éxito", mensaje)
            ventana.destroy()
        else:
            messagebox.showerror("Error", mensaje)

    tk.Button(ventana, text="Guardar", command=on_submit).pack(pady=20)
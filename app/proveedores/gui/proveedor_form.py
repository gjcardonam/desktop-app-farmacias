import tkinter as tk
from tkinter import messagebox
from app.proveedores.services.proveedor_service import procesar_nuevo_proveedor
from utils.ui_utils import centrar_ventana

def mostrar_formulario_proveedor(root):
    ventana = tk.Toplevel(root)
    ventana.title("Nuevo Proveedor")
    ventana.geometry("400x300")
    centrar_ventana(ventana, 400, 300)

    campos = {
        "Nombre": tk.Entry(ventana),
        "Documento": tk.Entry(ventana),
        "Teléfono": tk.Entry(ventana),
        "Email": tk.Entry(ventana)
    }

    for i, (label, entry) in enumerate(campos.items()):
        tk.Label(ventana, text=label).grid(row=i, column=0, padx=10, pady=5, sticky="w")
        entry.grid(row=i, column=1, padx=10, pady=5)

    def guardar():
        datos = [entry.get() for entry in campos.values()]
        ok, msg = procesar_nuevo_proveedor(*datos)
        if ok:
            messagebox.showinfo("Éxito", msg)
            ventana.destroy()
        else:
            messagebox.showerror("Error", msg)

    tk.Button(ventana, text="Guardar", command=guardar).grid(row=len(campos), columnspan=2, pady=10)
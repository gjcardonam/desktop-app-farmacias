import tkinter as tk
from tkinter import messagebox
from app.proveedores.services.proveedor_service import obtener_proveedor_por_id, actualizar_proveedor
from utils.ui_utils import centrar_ventana

def mostrar_formulario_edicion_proveedor(root, proveedor_id, callback=None):
    proveedor = obtener_proveedor_por_id(proveedor_id)
    if not proveedor:
        messagebox.showerror("Error", "Proveedor no encontrado.")
        return

    ventana = tk.Toplevel(root)
    ventana.title(f"Editar Proveedor #{proveedor_id}")
    ventana.geometry("400x300")
    centrar_ventana(ventana, 400, 300)

    campos = {
        "Nombre": tk.Entry(ventana),
        "Documento": tk.Entry(ventana),
        "Teléfono": tk.Entry(ventana),
        "Email": tk.Entry(ventana)
    }

    valores = [proveedor["nombre"], proveedor["documento"], proveedor["telefono"], proveedor["email"]]
    for i, (label, entry) in enumerate(campos.items()):
        tk.Label(ventana, text=label).grid(row=i, column=0, padx=10, pady=5, sticky="w")
        entry.insert(0, valores[i])
        entry.grid(row=i, column=1, padx=10, pady=5)

    def guardar():
        datos = [entry.get() for entry in campos.values()]
        ok, msg = actualizar_proveedor(proveedor_id, *datos)
        if ok:
            messagebox.showinfo("Éxito", msg)
            ventana.destroy()
            if callback:
                callback()
        else:
            messagebox.showerror("Error", msg)

    tk.Button(ventana, text="Guardar cambios", command=guardar).grid(row=len(campos), columnspan=2, pady=10)
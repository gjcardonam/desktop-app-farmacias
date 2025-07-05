import tkinter as tk
from tkinter import messagebox
from services.farmacia_service import obtener_farmacia_por_id, actualizar_farmacia

def mostrar_formulario_edicion_farmacia(root, farmacia_id, on_update_callback=None):
    farmacia = obtener_farmacia_por_id(farmacia_id)
    if not farmacia:
        messagebox.showerror("Error", "Farmacia no encontrada")
        return

    ventana = tk.Toplevel(root)
    ventana.title("Editar Farmacia")
    ventana.geometry("400x300")

    tk.Label(ventana, text="Nombre:").pack(pady=5)
    entry_nombre = tk.Entry(ventana, width=40)
    entry_nombre.insert(0, farmacia["nombre"])
    entry_nombre.pack()

    tk.Label(ventana, text="NIT:").pack(pady=5)
    entry_nit = tk.Entry(ventana, width=40)
    entry_nit.insert(0, farmacia["nit"])
    entry_nit.pack()

    tk.Label(ventana, text="Dirección:").pack(pady=5)
    entry_direccion = tk.Entry(ventana, width=40)
    entry_direccion.insert(0, farmacia["direccion"])
    entry_direccion.pack()

    tk.Label(ventana, text="Teléfono:").pack(pady=5)
    entry_telefono = tk.Entry(ventana, width=40)
    entry_telefono.insert(0, farmacia["telefono"])
    entry_telefono.pack()

    def on_submit():
        nombre = entry_nombre.get()
        nit = entry_nit.get()
        direccion = entry_direccion.get()
        telefono = entry_telefono.get()
        exito, mensaje = actualizar_farmacia(farmacia_id, nombre, nit, direccion, telefono)
        if exito:
            messagebox.showinfo("Éxito", mensaje)
            if on_update_callback:
                on_update_callback()
            ventana.destroy()
        else:
            messagebox.showerror("Error", mensaje)

    tk.Button(ventana, text="Guardar Cambios", command=on_submit).pack(pady=20)
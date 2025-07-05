import tkinter as tk
from tkinter import messagebox
from services.cliente_service import obtener_cliente_por_id, actualizar_cliente

def mostrar_formulario_edicion_cliente(root, cliente_id, on_update_callback=None):
    cliente = obtener_cliente_por_id(cliente_id)
    if not cliente:
        messagebox.showerror("Error", "Cliente no encontrado")
        return

    ventana = tk.Toplevel(root)
    ventana.title("Editar Cliente")
    ventana.geometry("400x300")

    tk.Label(ventana, text="Nombre:").pack(pady=5)
    entry_nombre = tk.Entry(ventana, width=40)
    entry_nombre.insert(0, cliente["nombre"])
    entry_nombre.pack()

    tk.Label(ventana, text="Documento:").pack(pady=5)
    entry_documento = tk.Entry(ventana, width=40)
    entry_documento.insert(0, cliente["documento"])
    entry_documento.pack()

    tk.Label(ventana, text="Teléfono:").pack(pady=5)
    entry_telefono = tk.Entry(ventana, width=40)
    entry_telefono.insert(0, cliente["telefono"])
    entry_telefono.pack()

    def on_submit():
        nombre = entry_nombre.get()
        documento = entry_documento.get()
        telefono = entry_telefono.get()
        exito, mensaje = actualizar_cliente(cliente_id, nombre, documento, telefono)
        if exito:
            messagebox.showinfo("Éxito", mensaje)
            if on_update_callback:
                on_update_callback()  # 🔁 Recargar el listado
            ventana.destroy()
        else:
            messagebox.showerror("Error", mensaje)

    tk.Button(ventana, text="Guardar Cambios", command=on_submit).pack(pady=20)
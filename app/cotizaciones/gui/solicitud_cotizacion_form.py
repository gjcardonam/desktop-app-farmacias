import tkinter as tk
from tkinter import messagebox
from app.cotizaciones.services.solicitud_cotizacion_service import crear_solicitud_cotizacion
from app.cotizaciones.gui.seleccionar_proveedores import seleccionar_proveedores
from utils.ui_utils import centrar_ventana

def mostrar_formulario_solicitud(root):
    ventana = tk.Toplevel(root)
    ventana.title("Crear Solicitud de Cotización")
    ventana.geometry("400x400")
    centrar_ventana(ventana, 400, 400)

    tk.Label(ventana, text="ID Sucursal:").pack(pady=5)
    entry_sucursal = tk.Entry(ventana, width=40)
    entry_sucursal.pack()

    tk.Label(ventana, text="ID Usuario:").pack(pady=5)
    entry_usuario = tk.Entry(ventana, width=40)
    entry_usuario.pack()

    tk.Label(ventana, text="Observaciones:").pack(pady=5)
    entry_obs = tk.Entry(ventana, width=40)
    entry_obs.pack()

    tk.Label(ventana, text="Items (id_producto,cantidad):").pack(pady=5)
    entry_items = tk.Entry(ventana, width=40)
    entry_items.pack()

    def on_submit():
        try:
            items_raw = entry_items.get().split(";")
            items = []
            for item in items_raw:
                prod, cant = item.split(",")
                items.append({"id_producto": int(prod), "cantidad": int(cant)})

            # crear_solicitud_cotizacion debe devolver (exito, mensaje, solicitud_id)
            exito, mensaje, solicitud_id = crear_solicitud_cotizacion(
                int(entry_sucursal.get()),
                int(entry_usuario.get()),
                items,
                entry_obs.get()
            )

            if exito:
                messagebox.showinfo("Éxito", mensaje)
                ventana.destroy()
                # Llamar a la ventana para seleccionar proveedores
                seleccionar_proveedores(root, solicitud_id)
            else:
                messagebox.showerror("Error", mensaje)
        except Exception as e:
            messagebox.showerror("Error", f"Formato de items inválido: {str(e)}")

    tk.Button(ventana, text="Guardar", command=on_submit).pack(pady=20)
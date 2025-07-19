import tkinter as tk
from tkinter import messagebox
from app.proveedores.repository.proveedor_repository import obtener_proveedores
from app.cotizaciones.services.solicitud_cotizacion_service import enviar_solicitud_a_proveedores
from utils.ui_utils import centrar_ventana

def seleccionar_proveedores(root, solicitud_id):
    ventana = tk.Toplevel(root)
    ventana.title("Seleccionar Proveedores")
    ventana.geometry("400x400")
    centrar_ventana(ventana, 400, 400)

    tk.Label(ventana, text=f"Solicitud {solicitud_id}: Selecciona los proveedores", font=("Helvetica", 12, "bold")).pack(pady=10)

    proveedores = obtener_proveedores()
    check_vars = []

    frame_lista = tk.Frame(ventana)
    frame_lista.pack(fill="both", expand=True, pady=10)

    for prov in proveedores:
        var = tk.IntVar()
        chk = tk.Checkbutton(frame_lista, text=f"{prov['nombre']} (ID: {prov['id']})", variable=var)
        chk.pack(anchor="w")
        check_vars.append((prov['id'], var))

    def on_confirm():
        seleccionados = [pid for pid, var in check_vars if var.get() == 1]
        if not seleccionados:
            messagebox.showwarning("Aviso", "No seleccionaste ningún proveedor.")
            return
        exito, mensaje = enviar_solicitud_a_proveedores(solicitud_id, seleccionados)
        if exito:
            messagebox.showinfo("Éxito", mensaje)
            ventana.destroy()
        else:
            messagebox.showerror("Error", mensaje)

    tk.Button(ventana, text="Enviar Solicitud", command=on_confirm).pack(pady=10)
import tkinter as tk
from tkinter import ttk
from app.cotizaciones.services.solicitud_cotizacion_service import listar_solicitudes
from utils.ui_utils import centrar_ventana

def mostrar_listado_solicitudes(root):
    ventana = tk.Toplevel(root)
    ventana.title("Listado de Solicitudes de Cotización")
    ventana.geometry("600x400")
    centrar_ventana(ventana, 600, 400)

    tree = ttk.Treeview(ventana, columns=("ID", "Fecha", "Estado", "Observaciones"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Fecha", text="Fecha")
    tree.heading("Estado", text="Estado")
    tree.heading("Observaciones", text="Observaciones")
    tree.pack(fill="both", expand=True)

    for sc in listar_solicitudes():
        tree.insert("", "end", values=(sc["id"], sc["fecha_creacion"], sc["estado"], sc["observaciones"]))
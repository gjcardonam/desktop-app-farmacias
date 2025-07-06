# gui/listado_facturas.py

import tkinter as tk
from tkinter import ttk
from app.facturas.services.factura_service import obtener_facturas
from app.facturas.services.factura_service import obtener_detalle_factura
from utils.ui_utils import centrar_ventana

def mostrar_detalle_factura(factura_id, root):
    detalles = obtener_detalle_factura(factura_id)

    ventana = tk.Toplevel(root)
    ventana.title(f"Detalle de Factura #{factura_id}")
    ventana.geometry("600x450")
    centrar_ventana(ventana, 600, 450)

    tree = ttk.Treeview(ventana, columns=("producto", "cantidad", "precio_unit", "impuesto", "subtotal"), show="headings")
    tree.heading("producto", text="Producto")
    tree.heading("cantidad", text="Cantidad")
    tree.heading("precio_unit", text="Precio Unitario")
    tree.heading("impuesto", text="Impuesto")
    tree.heading("subtotal", text="Subtotal")

    total = 0
    for item in detalles:
        cantidad = item["cantidad"]
        precio = item["precio_unit"]
        subtotal = cantidad * precio
        total += subtotal
        tree.insert("", "end", values=(
            item["producto"],
            cantidad,
            f"${precio:,.2f}",
            f"${item['impuesto']:,.2f}",
            f"${subtotal:,.2f}"
        ))

    tree.pack(fill="both", expand=True, padx=10, pady=10)

    # Total al final
    label_total = tk.Label(ventana, text=f"Total: ${total:,.2f}", font=("Helvetica", 12, "bold"))
    label_total.pack(anchor="e", padx=20, pady=10)

def mostrar_listado_facturas(root):
    ventana = tk.Toplevel(root)
    ventana.title("Listado de Facturas")
    ventana.geometry("800x600")

    tree = ttk.Treeview(ventana, columns=("id", "cliente", "usuario", "fecha", "total", "estado"), show="headings")
    tree.heading("id", text="ID")
    tree.heading("cliente", text="Cliente")
    tree.heading("usuario", text="Usuario")
    tree.heading("fecha", text="Fecha")
    tree.heading("total", text="Total")
    tree.heading("estado", text="Estado")
    
    tree.pack(fill="both", expand=True)

    facturas = obtener_facturas()
    for f in facturas:
        tree.insert("", "end", values=(f["id"], f["cliente"], f["usuario"], f["fecha"], f["total"], f["estado"]))

    def on_double_click(event):
        item = tree.focus()
        if not item:
            return
        factura_id = tree.item(item)["values"][0]
        mostrar_detalle_factura(factura_id, root)

    tree.bind("<Double-1>", on_double_click)
import tkinter as tk
from tkinter import ttk

from app.facturas.services.factura_service import (
    obtener_facturas,
    obtener_detalle_factura,
)
from utils.treeview_helpers import bind_treeview_activate
from utils.ui_utils import centrar_ventana


# --------------------------------------------------------------------------- #
#  Ventana de DETALLE de una factura                                          #
# --------------------------------------------------------------------------- #
def mostrar_detalle_factura(factura_id: int, root: tk.Tk) -> None:
    detalles = obtener_detalle_factura(factura_id)

    ventana = tk.Toplevel(root)
    ventana.title(f"Detalle de Factura #{factura_id}")
    ventana.geometry("600x450")
    centrar_ventana(ventana, 600, 450)

    tree = ttk.Treeview(
        ventana,
        columns=("producto", "cantidad", "precio_unit", "impuesto", "subtotal"),
        show="headings",
    )
    tree.heading("producto", text="Producto")
    tree.heading("cantidad", text="Cantidad")
    tree.heading("precio_unit", text="Precio Unit.")
    tree.heading("impuesto", text="Impuesto")
    tree.heading("subtotal", text="Subtotal")

    total = 0
    for item in detalles:
        cantidad = item["cantidad"]
        precio = item["precio_unit"]
        subtotal = cantidad * precio
        total += subtotal
        tree.insert(
            "",
            "end",
            values=(
                item["producto"],
                cantidad,
                f"${precio:,.2f}",
                f"${item['impuesto']:,.2f}",
                f"${subtotal:,.2f}",
            ),
        )

    tree.pack(fill="both", expand=True, padx=10, pady=10)

    tk.Label(
        ventana,
        text=f"Total: ${total:,.2f}",
        font=("Helvetica", 12, "bold"),
    ).pack(anchor="e", padx=20, pady=10)


# --------------------------------------------------------------------------- #
#  Ventana de LISTADO de facturas                                             #
# --------------------------------------------------------------------------- #
def mostrar_listado_facturas(root: tk.Tk) -> None:
    ventana = tk.Toplevel(root)
    ventana.title("Listado de Facturas")
    ventana.geometry("800x600")
    centrar_ventana(ventana, 800, 600)

    columnas = ("id", "cliente", "usuario", "fecha", "total", "estado")
    tree = ttk.Treeview(ventana, columns=columnas, show="headings")

    for col in columnas:
        tree.heading(col, text=col.capitalize())
        tree.column(col, width=130)

    tree.pack(fill="both", expand=True, padx=10, pady=10)

    # carga / recarga
    def cargar_facturas():
        tree.delete(*tree.get_children())           # limpia
        for f in obtener_facturas():
            tree.insert(
                "",
                "end",
                values=(
                    f["id"],
                    f["cliente"],
                    f["usuario"],
                    f["fecha"],
                    f["total"],
                    f["estado"],
                ),
            )

    # vínculo Enter + clic
    bind_treeview_activate(
        tree,
        lambda factura_id: mostrar_detalle_factura(factura_id, root)
    )

    cargar_facturas()

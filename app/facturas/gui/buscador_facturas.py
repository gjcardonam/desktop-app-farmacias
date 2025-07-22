import tkinter as tk
from tkinter import ttk
from app.facturas.services.factura_service import obtener_todas_las_facturas
from utils.ui_utils import centrar_ventana

def mostrar_buscador_facturas(root):
    ventana = tk.Toplevel(root)
    ventana.title("Buscador de facturas")
    ventana.geometry("800x400")
    centrar_ventana(ventana, 800, 400)

    tk.Label(ventana, text="Buscar factura por id:").pack(pady=5)
    entry_busqueda = tk.Entry(ventana, width=50)
    entry_busqueda.pack()

    columnas = ("id", "cliente", "usuario", "fecha", "total" ,"estado")
    tree = ttk.Treeview(ventana, columns=columnas, show="headings")

    for col in columnas:
        tree.heading(col, text=col.replace("_", " ").capitalize())
        tree.column(col, width=150)

    def     cargar_facturas_filtradas():
        query = entry_busqueda.get().strip().lower()
        tree.delete(*tree.get_children())

        if not query:
            return

        facturas = obtener_todas_las_facturas()
        for factura in facturas:
            if query in str(factura["id"]):
                total = float(str(factura["total"]).replace("$", "").replace(",", ""))
                tree.insert("", "end", values=(
                    factura["cliente"],
                    factura["usuario"],
                    factura["fecha"],
                    f"{total:,.2f}",
                    factura["estado"]
                ))

    tk.Button(ventana, text="Buscar", command=cargar_facturas_filtradas).pack(pady=5)
    tree.pack(expand=True, fill="both", padx=10, pady=10)

    cargar_facturas_filtradas()
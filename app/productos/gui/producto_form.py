import tkinter as tk
from tkinter import ttk, messagebox
from app.productos.services.producto_service import procesar_nuevo_producto
from app.farmacias.services.farmacia_service import obtener_farmacias
from utils.ui_utils import centrar_ventana

def mostrar_formulario_producto(root):
    ventana = tk.Toplevel(root)
    ventana.title("Agregar Producto")
    ventana.geometry("500x450")
    centrar_ventana(ventana, 500, 450)

    tk.Label(ventana, text="Nombre:").pack(pady=5)
    entry_nombre = tk.Entry(ventana, width=50)
    entry_nombre.pack()

    tk.Label(ventana, text="Descripción:").pack(pady=5)
    entry_descripcion = tk.Entry(ventana, width=50)
    entry_descripcion.pack()

    tk.Label(ventana, text="Precio de venta:").pack(pady=5)
    entry_precio = tk.Entry(ventana, width=20)
    entry_precio.pack()

    tk.Label(ventana, text="Costo:").pack(pady=5)
    entry_costo = tk.Entry(ventana, width=20)
    entry_costo.pack()

    tk.Label(ventana, text="Stock inicial:").pack(pady=5)
    entry_stock = tk.Entry(ventana, width=20)
    entry_stock.pack()

    tk.Label(ventana, text="Farmacia:").pack(pady=5)
    combo_farmacia = ttk.Combobox(ventana, state="readonly", width=47)
    farmacias = obtener_farmacias()
    combo_farmacia["values"] = [f"{f['id']}: {f['nombre']}" for f in farmacias]
    combo_farmacia.pack()

    def on_submit():
        try:
            nombre = entry_nombre.get()
            descripcion = entry_descripcion.get()
            precio = float(entry_precio.get())
            costo = float(entry_costo.get())
            stock = int(entry_stock.get())
            id_farmacia = int(combo_farmacia.get().split(":")[0])
            exito, mensaje = procesar_nuevo_producto(nombre, descripcion, precio, costo, stock, id_farmacia)
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                ventana.destroy()
            else:
                messagebox.showerror("Error", mensaje)
        except Exception as e:
            messagebox.showerror("Error", f"Error de entrada: {str(e)}")

    tk.Button(ventana, text="Guardar", command=on_submit).pack(pady=20)
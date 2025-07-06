import tkinter as tk
from tkinter import ttk, messagebox
from app.productos.services.producto_service import obtener_producto_por_id, actualizar_producto
from app.farmacias.services.farmacia_service import obtener_farmacias
from utils.ui_utils import centrar_ventana

def mostrar_formulario_edicion_producto(root, producto_id, on_update_callback=None):
    producto = obtener_producto_por_id(producto_id)
    if not producto:
        messagebox.showerror("Error", "Producto no encontrado")
        return

    ventana = tk.Toplevel(root)
    ventana.title("Editar Producto")
    ventana.geometry("500x450")
    centrar_ventana(ventana, 500, 450)

    tk.Label(ventana, text="Nombre:").pack(pady=5)
    entry_nombre = tk.Entry(ventana, width=50)
    entry_nombre.insert(0, producto["nombre"])
    entry_nombre.pack()

    tk.Label(ventana, text="Descripción:").pack(pady=5)
    entry_descripcion = tk.Entry(ventana, width=50)
    entry_descripcion.insert(0, producto["descripcion"])
    entry_descripcion.pack()

    tk.Label(ventana, text="Precio de venta:").pack(pady=5)
    entry_precio = tk.Entry(ventana, width=20)
    entry_precio.insert(0, str(producto["precio_venta"]))
    entry_precio.pack()

    tk.Label(ventana, text="Costo:").pack(pady=5)
    entry_costo = tk.Entry(ventana, width=20)
    entry_costo.insert(0, str(producto["costo"]))
    entry_costo.pack()

    tk.Label(ventana, text="Stock:").pack(pady=5)
    entry_stock = tk.Entry(ventana, width=20)
    entry_stock.insert(0, str(producto["stock"]))
    entry_stock.pack()

    tk.Label(ventana, text="Farmacia:").pack(pady=5)
    combo_farmacia = ttk.Combobox(ventana, state="readonly", width=47)
    farmacias = obtener_farmacias()
    combo_farmacia["values"] = [f"{f['id']}: {f['nombre']}" for f in farmacias]
    combo_farmacia.set(f"{producto['id_farmacia']}: {producto['farmacia']}")
    combo_farmacia.pack()

    def on_submit():
        try:
            nombre = entry_nombre.get()
            descripcion = entry_descripcion.get()
            precio = float(entry_precio.get())
            costo = float(entry_costo.get())
            stock = int(entry_stock.get())
            id_farmacia = int(combo_farmacia.get().split(":")[0])
            exito, mensaje = actualizar_producto(producto_id, nombre, descripcion, precio, costo, stock, id_farmacia)
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                if on_update_callback:
                    on_update_callback()
                ventana.destroy()
            else:
                messagebox.showerror("Error", mensaje)
        except Exception as e:
            messagebox.showerror("Error", f"Entrada inválida: {str(e)}")

    tk.Button(ventana, text="Guardar Cambios", command=on_submit).pack(pady=20)
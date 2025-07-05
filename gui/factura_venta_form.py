import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from services.factura_service import registrar_factura
from services.cliente_service import obtener_todos_los_clientes
from services.producto_service import obtener_todos_los_productos

def mostrar_formulario_factura(root):
    ventana = tk.Toplevel(root)
    ventana.title("Registrar Factura de Venta")
    ventana.geometry("700x600")

    # --- Cliente ---
    tk.Label(ventana, text="Cliente:").pack(pady=5)
    combo_cliente = ttk.Combobox(ventana, state="readonly", width=50)
    clientes = obtener_todos_los_clientes()
    combo_cliente["values"] = [f"{c['id']}: {c['nombre']}" for c in clientes]
    combo_cliente.pack()

    # --- Tabla de productos ---
    frame_productos = tk.Frame(ventana)
    frame_productos.pack(pady=10, fill="both", expand=True)

    tree = ttk.Treeview(frame_productos, columns=("id", "nombre", "precio", "cantidad"), show="headings")
    tree.heading("id", text="ID")
    tree.heading("nombre", text="Producto")
    tree.heading("precio", text="Precio")
    tree.heading("cantidad", text="Cantidad")
    tree.column("cantidad", width=80)

    productos = obtener_todos_los_productos()
    for p in productos:
        tree.insert("", "end", values=(p["id"], p["nombre"], p["precio_venta"], 0))
    tree.pack(fill="both", expand=True)

    # --- Total ---
    label_total = tk.Label(ventana, text="Total: $0", font=("Helvetica", 12))
    label_total.pack(pady=10)

    def calcular_total():
        total = 0
        for item in tree.get_children():
            values = tree.item(item, "values")
            try:
                cantidad = int(values[3])
                precio = float(values[2])
                total += cantidad * precio
            except:
                continue
        label_total.config(text=f"Total: ${total:,.2f}")

    def on_edit_quantity(event):
        item = tree.focus()
        if not item:
            return
        values = list(tree.item(item, "values"))
        cantidad = tk.simpledialog.askinteger("Cantidad", f"Ingrese cantidad para '{values[1]}':", minvalue=0)
        if cantidad is not None:
            values[3] = cantidad
            tree.item(item, values=values)
            calcular_total()

    tree.bind("<Double-1>", on_edit_quantity)

    def on_submit():
        if not combo_cliente.get():
            messagebox.showerror("Error", "Debes seleccionar un cliente")
            return

        id_cliente = int(combo_cliente.get().split(":")[0])
        productos_factura = []

        for item in tree.get_children():
            id_producto, _, precio, cantidad = tree.item(item, "values")
            cantidad = int(cantidad)
            if cantidad > 0:
                productos_factura.append({
                    "producto_id": int(id_producto),
                    "cantidad": cantidad,
                    "precio": float(precio)
                })

        if not productos_factura:
            messagebox.showerror("Error", "Debes agregar al menos un producto")
            return

        exito, respuesta = registrar_factura(id_cliente, productos_factura)
        if exito:
            messagebox.showinfo("Éxito", f"Factura #{respuesta['factura_id']} creada por ${respuesta['total']:,}")
            ventana.destroy()
        else:
            messagebox.showerror("Error", respuesta)
            
    tk.Button(ventana, text="Guardar Factura", command=on_submit).pack(pady=10)
import tkinter as tk
from tkinter import ttk
from app.usuarios.services.usuario_service import obtener_todos_los_usuarios
from app.usuarios.gui.editar_usuario_form import mostrar_formulario_edicion_usuario
from utils.ui_utils import centrar_ventana

def mostrar_buscador_usuarios(root):
    ventana = tk.Toplevel(root)
    ventana.title("Buscador de usuarios")
    ventana.geometry("800x400")
    centrar_ventana(ventana, 800, 400)

    tk.Label(ventana, text="Buscar usuario por nombre:").pack(pady=5)
    entry_busqueda = tk.Entry(ventana, width=50)
    entry_busqueda.pack()

    columnas = ("id", "nombre", "email")
    tree = ttk.Treeview(ventana, columns=columnas, show="headings")

    for col in columnas:
        tree.heading(col, text=col.replace("_", " ").capitalize())
        tree.column(col, width=150)

    def cargar_usuarios_filtrados():
        query = entry_busqueda.get().strip().lower()
        tree.delete(*tree.get_children())

        if not query:
            return

        usuarios = obtener_todos_los_usuarios()
        for usuario in usuarios:
            if query in usuario["nombre"].lower():
                tree.insert("", "end", values=(
                    usuario["id"],
                    usuario["nombre"],
                    usuario["email"]
                ))

    def on_activate(event):
        item = tree.selection()
        if item:
            valores = tree.item(item[0], "values")
            usuario_id = int(valores[0])
            mostrar_formulario_edicion_usuario(root, usuario_id, cargar_usuarios_filtrados)

    tree.bind("<<TreeviewActivate>>", on_activate)

    tk.Button(ventana, text="Buscar", command=cargar_usuarios_filtrados).pack(pady=5)
    tree.pack(expand=True, fill="both", padx=10, pady=10)

    cargar_usuarios_filtrados()
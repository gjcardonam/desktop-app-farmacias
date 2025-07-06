import tkinter as tk
from tkinter import ttk
from app.usuarios.services.usuario_service import obtener_todos_los_usuarios
from app.usuarios.gui.editar_usuario_form import mostrar_formulario_edicion_usuario
from utils.ui_utils import centrar_ventana

def mostrar_listado_usuarios(root):
    ventana = tk.Toplevel(root)
    ventana.title("Listado de Usuarios")
    ventana.geometry("600x400")
    centrar_ventana(ventana, 600, 400)

    columnas = ("id", "nombre", "email")
    tree = ttk.Treeview(ventana, columns=columnas, show="headings")

    for col in columnas:
        tree.heading(col, text=col.capitalize())
        tree.column(col, width=150)

    def cargar_usuarios():
        for i in tree.get_children():
            tree.delete(i)
        usuarios = obtener_todos_los_usuarios()
        for u in usuarios:
            tree.insert("", "end", values=(u["id"], u["nombre"], u["email"]))

    cargar_usuarios()
    tree.pack(expand=True, fill="both", padx=10, pady=10)

    def on_double_click(event):
        item = tree.selection()
        if item:
            valores = tree.item(item[0], "values")
            usuario_id = int(valores[0])
            mostrar_formulario_edicion_usuario(root, usuario_id, cargar_usuarios)

    tree.bind("<Double-1>", on_double_click)
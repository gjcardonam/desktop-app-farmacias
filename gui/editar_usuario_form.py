import tkinter as tk
from tkinter import messagebox
from services.usuario_service import obtener_usuario, procesar_actualizacion_usuario
from utils.ui_utils import centrar_ventana

def mostrar_formulario_edicion_usuario(root, usuario_id, on_update_callback=None):
    usuario = obtener_usuario(usuario_id)
    if not usuario:
        messagebox.showerror("Error", "Usuario no encontrado")
        return

    ventana = tk.Toplevel(root)
    ventana.title("Editar Usuario")
    ventana.geometry("400x400")
    centrar_ventana(ventana, 400, 400)

    # Nombre
    tk.Label(ventana, text="Nombre:").pack(pady=5)
    entry_nombre = tk.Entry(ventana)
    entry_nombre.insert(0, usuario["nombre"])
    entry_nombre.pack()

    # Email
    tk.Label(ventana, text="Email:").pack(pady=5)
    entry_email = tk.Entry(ventana)
    entry_email.insert(0, usuario["email"])
    entry_email.pack()

    # Rol
    tk.Label(ventana, text="Rol:").pack(pady=5)
    rol_var = tk.StringVar(ventana)
    rol_var.set(usuario["rol"])
    tk.OptionMenu(ventana, rol_var, "admin", "vendedor").pack()

    # Activo
    tk.Label(ventana, text="Estado:").pack(pady=5)
    activo_var = tk.BooleanVar(ventana)
    activo_var.set(usuario["activo"])
    tk.Checkbutton(ventana, text="Activo", variable=activo_var).pack()

    # Contraseña (opcional)
    tk.Label(ventana, text="Contraseña (opcional):").pack(pady=5)
    entry_password = tk.Entry(ventana, show="*")
    entry_password.pack()

    def on_submit():
        nombre = entry_nombre.get()
        email = entry_email.get()
        rol = rol_var.get()
        activo = activo_var.get()
        password = entry_password.get()

        # La contraseña es opcional, pero no la pasamos al update si está vacía
        exito, mensaje = procesar_actualizacion_usuario(
            usuario_id, nombre, email, rol, activo, password if password else None
        )

        if exito:
            messagebox.showinfo("Éxito", mensaje)
            ventana.destroy()
            if on_update_callback:
                on_update_callback()
        else:
            messagebox.showerror("Error", mensaje)

    tk.Button(ventana, text="Guardar Cambios", command=on_submit).pack(pady=20)
import tkinter as tk

def centrar_ventana(ventana, ancho, alto):
    ventana.update_idletasks()
    pantalla_ancho = ventana.winfo_screenwidth()
    pantalla_alto = ventana.winfo_screenheight()

    x = (pantalla_ancho // 2) - (ancho // 2)
    y = (pantalla_alto // 2) - (alto // 2)
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")
    
def activar_enter_en_todos_los_botones(root: tk.Tk) -> None:
    """
    Hace que cualquier tk.Button o ttk.Button invoque su command
    cuando el usuario pulse la tecla Return/Enter estando el foco
    sobre el botón.
    Debe llamarse una única vez después de crear la ventana raíz.
    """
    for clase in ("Button", "TButton"):
        # Si el foco está sobre un botón y se pulsa Enter, ejecuta .invoke()
        root.bind_class(clase, "<Return>",
                        lambda e: e.widget.invoke(), add="+")
        
def permitir_tab_en_botones(root: tk.Tk) -> None:
    """
    Hace que cualquier tk.Button o ttk.Button pueda recibir el foco
    al tabular, en toda la aplicación.
    """
    # Para widgets clásicos de Tk
    root.option_add("*Button.takefocus", "1")
    # Para widgets themed de Ttk
    root.option_add("*TButton.takefocus", "1")
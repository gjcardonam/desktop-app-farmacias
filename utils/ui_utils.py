import tkinter as tk
import tkinter.ttk as ttk   # para los type-hints de Treeview y Button


# ────────────────────────────────────
#  Colocar ventana en el centro
# ────────────────────────────────────
def centrar_ventana(ventana: tk.Toplevel | tk.Tk, ancho: int, alto: int) -> None:
    ventana.update_idletasks()
    pant_ancho = ventana.winfo_screenwidth()
    pant_alto = ventana.winfo_screenheight()
    x = (pant_ancho // 2) - (ancho // 2)
    y = (pant_alto // 2) - (alto // 2)
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")


# ────────────────────────────────────
#  Accesibilidad → botones
# ────────────────────────────────────
def permitir_tab_en_botones(root: tk.Tk) -> None:
    """Hace que Tab/Shift-Tab puedan visitar todos los botones."""
    root.option_add("*Button.takefocus", "1")
    root.option_add("*TButton.takefocus", "1")


def activar_enter_en_todos_los_botones(root: tk.Tk) -> None:
    """Enter sobre un botón con foco llama a .invoke() (igual que Space)."""
    root.bind_class(
        "TButton", "<Return>",
        lambda e: e.widget.invoke(),
        add="+"
    )
    root.bind_class(
        "Button", "<Return>",
        lambda e: e.widget.invoke(),
        add="+"
    )


# ────────────────────────────────────
#  Treeview helpers (selección + atajos)
# ────────────────────────────────────
def _limpiar_seleccion(tree: ttk.Treeview) -> None:
    """Quita cualquier selección y foco en el Treeview."""
    tree.selection_remove(tree.selection())
    tree.focus("")


def activar_enter_en_treeviews(
    root: tk.Tk,
    *,
    doble_clic: bool = False,
) -> None:
    """
    • Clic (simple o doble, según `doble_clic`) sobre fila → selecciona y emite <<TreeviewActivate>>
    • Clic en zona vacía                                  → des-selecciona filas
    • Tecla Enter con foco en Treeview                    → emite <<TreeviewActivate>>
    • Tecla Esc                                           → des-selecciona filas
    """
    def _clic(event: tk.Event) -> None:
        tree: ttk.Treeview = event.widget
        fila = tree.identify_row(event.y)

        if fila:                       # clic sobre fila válida
            tree.selection_set(fila)
            tree.focus(fila)
            tree.event_generate("<<TreeviewActivate>>")
        else:                          # clic fuera de filas
            _limpiar_seleccion(tree)

    # ── Disparador por ratón ─────────────────────────────────────────────
    evento_raton = "<Double-Button-1>" if doble_clic else "<ButtonRelease-1>"
    root.bind_class("Treeview", evento_raton, _clic, add="+")

    # ── Atajo de teclado: Enter ─────────────────────────────────────────
    root.bind_class(
        "Treeview", "<Return>",
        lambda e: e.widget.event_generate("<<TreeviewActivate>>"),
        add="+",
    )

    # ── Atajo de teclado: Esc → limpiar selección ──────────────────────
    root.bind_class(
        "Treeview", "<Escape>",
        lambda e: _limpiar_seleccion(e.widget),
        add="+",
    )

    # ── Permitir que Tab entre al Treeview ─────────────────────────────
    root.option_add("*Treeview.takefocus", "1")
import tkinter as tk
import tkinter.ttk as ttk 
from typing import Callable, Any

def get_row_id(event: tk.Event, id_col: int = 0) -> int | None:
    tree: ttk.Treeview = event.widget

    # 1. Intenta por coordenada (ratón)
    row = tree.identify_row(event.y)

    # 2. Si falla (Enter o clic muy rápido), usa la selección
    if not row:
        sel = tree.selection()
        if sel:
            row = sel[0]

    if not row:
        return None  # no hay fila válida

    values = tree.item(row, "values")
    try:
        return int(values[id_col])
    except (IndexError, ValueError):
        return None

def bind_treeview_activate(
    tree: tk.ttk.Treeview,
    callback: Callable[[int], Any],
    *,
    id_col: int = 0,
) -> None:
    """
    Enlaza el Treeview para que <<TreeviewActivate>> invoque `callback(id)`
    donde `id` es el valor de la columna `id_col`.
    """
    def _handler(event):
        id_ = get_row_id(event, id_col=id_col)
        if id_ is not None:
            callback(id_)

    tree.bind("<<TreeviewActivate>>", _handler)

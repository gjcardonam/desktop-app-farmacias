import tkinter as tk
from typing import Callable, Any

def get_row_id(event: tk.Event, id_col: int = 0) -> int | None:
    """
    Devuelve el valor (int) de la columna `id_col` de la fila bajo el cursor.
    Si el clic fue en una zona vacía → des-selecciona y retorna None.
    """
    tree = event.widget
    row = tree.identify_row(event.y)

    if not row:                       # zona vacía
        tree.selection_remove(tree.selection())
        return None

    tree.selection_set(row)           # marca la fila clicada
    values = tree.item(row, "values")
    return int(values[id_col])

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

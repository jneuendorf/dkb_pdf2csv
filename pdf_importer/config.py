from .transform_emit import transform_emit


config = dict(
    parser=dict(
        alignment=None,
        header_row_labels=None,
        column_x_tolerance=1.0,
        max_missing_cells_per_row=1,
    ),
    transform_emit=transform_emit,
)

import flask_table as ft


def get_ftable(keys, rows):
    DynamicTable = ft.create_table('dynamic',
                                   options={'classes': ('table', 'table-striped', 'table-bordered')})
    for col_name in keys:
        DynamicTable.add_column(col_name, ft.Col(col_name))

    dynamic_table = DynamicTable(rows)

    return dynamic_table

import sqlite3

from table2ascii import Alignment, PresetStyle, TableStyle
from table2ascii import table2ascii as t2a


def connect_to_db():
    conn = sqlite3.connect('./sqlite.db')
    cursor = conn.cursor()
    return cursor


def get_points_table(headers, body):
    return t2a(
        header=headers,
        body=body,
        style=PresetStyle.simple,
        alignments=[Alignment.LEFT, Alignment.RIGHT, Alignment.LEFT, Alignment.CENTER],
    )


def get_teams_table(headers, body):
    return t2a(
        header=headers,
        body=body,
        style=TableStyle.from_string(" ═     ║ ═                    "),
        alignments=[Alignment.CENTER, Alignment.CENTER],
    )
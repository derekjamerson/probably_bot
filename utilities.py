import random
import sqlite3

from table2ascii import Alignment, PresetStyle, TableStyle
from table2ascii import table2ascii as t2a

THUMBS_UP = '👍'
THUMBS_DOWN = '👎'


def calc_win_rate(wins, games):
    wins = int(wins)
    games = int(games)
    if not games:
        return -1

    return wins / games


def connect_to_db():
    return sqlite3.connect('./sqlite.db')


def get_ism(conn):
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(
        """SELECT * FROM Isms""",
    )
    ism = random.choice(cursor.fetchall())
    result = f'"{ism["Quote"]}"'
    if ism['Person']:
        result += f' - {ism["Person"]}'
    return result


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

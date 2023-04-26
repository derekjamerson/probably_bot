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

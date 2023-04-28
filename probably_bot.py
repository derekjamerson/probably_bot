import json
import os
import random
import sqlite3

import discord
from discord.ext import commands
from dotenv import load_dotenv

from utilities import (
    THUMBS_DOWN,
    THUMBS_UP,
    calc_win_rate,
    connect_to_db,
    get_ism,
    get_points_table,
    get_teams_table,
)

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)
working_ctx = None


@bot.command(name='customs', help='Create 2 teams of 5')
async def customs(ctx):
    voice_state = ctx.author.voice

    if not voice_state:
        return

    member_names = [x.name for x in voice_state.channel.members]

    # # TESTING
    # member_names = [str(num) for num in range(10)]

    members_count = len(member_names)

    if members_count < 10:
        await ctx.message.add_reaction(THUMBS_DOWN)
        await ctx.channel.send(f'LF{10 - members_count}M Gold-Plat elo Customs')
        return
    if members_count > 10:
        await ctx.message.add_reaction(THUMBS_DOWN)
        await ctx.channel.send('Too many niggas!')
        return

    title = '*** Probably Customs ***'
    headers = ['Blue Team', 'Red Team']

    random.shuffle(member_names)
    blue_team = member_names[:5]
    red_team = member_names[5:]

    body = []
    for i in range(5):
        body.append([blue_team[i], red_team[i]])

    conn = connect_to_db()
    cursor = conn.cursor()

    sql_old = """
        UPDATE Current_Game
        SET Active = 0
    """
    cursor.execute(sql_old)

    sql_new = """
        INSERT INTO Current_Game (Blue, Red)
        VALUES (?, ?);
    """
    cursor.execute(sql_new, (json.dumps(blue_team), json.dumps(red_team)))

    ism = get_ism(conn)
    output = get_teams_table(headers, body)

    conn.commit()
    conn.close()

    await ctx.message.add_reaction(THUMBS_UP)
    await ctx.send(f"```\n{ism}\n\n{title}\n\n{output}\n```")


@bot.command(name='points', help='Display Magic Internet Points')
async def magic_internet_points(ctx):
    conn = connect_to_db()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM Magic_Internet_Points""")

    rows = cursor.fetchall()
    rows.sort(key=lambda x: calc_win_rate(x['Wins'], x['Games']))
    rows.reverse()

    headers = rows[0].keys()
    headers.append('Win Rate')

    body = []
    for row in rows:
        win_rate = calc_win_rate(row['Wins'], row['Games'])
        percent_string = '{:.2%}'.format(win_rate) if win_rate >= 0 else 'NEW'
        body.append([row['Name'], row['Wins'], row['Games'], percent_string])

    title = '*** Magic Internet Points ***'
    output = get_points_table(headers, body)
    ism = get_ism(conn)

    conn.close()
    await ctx.message.add_reaction(THUMBS_UP)
    await ctx.send(f"```\n{ism}\n\n{title}\n\n{output}\n```")


@bot.command(name='win', help='Record the winners of a game')
async def win(ctx):
    author = ctx.author.display_name

    # # TESTING
    # author = '1'

    conn = connect_to_db()
    conn.row_factory = sqlite3.Row
    cursor_query = conn.cursor()
    cursor_query.execute(
        """SELECT Blue, Red FROM Current_Game WHERE rowid = (SELECT MAX(rowid) FROM Current_Game) AND Active = 1""",
    )
    row = cursor_query.fetchone()

    if not row:
        await ctx.message.add_reaction(THUMBS_DOWN)
        return

    all_players = [player for team in row for player in json.loads(team)]
    winners = [json.loads(team) for team in row if author in team][0]

    if not winners:
        await ctx.message.add_reaction(THUMBS_DOWN)
        return

    cursor_result = conn.cursor()

    sql_insert = """
        INSERT OR IGNORE INTO Magic_Internet_Points (Name)
        VALUES (?);
    """
    cursor_result.executemany(sql_insert, all_players)

    sql_games = """
        UPDATE Magic_Internet_Points
        SET Games = Games + 1
        WHERE Name in (?,?,?,?,?,?,?,?,?,?);
    """
    cursor_result.execute(sql_games, all_players)

    sql_wins = """
        UPDATE Magic_Internet_Points
        SET Wins = Wins + 1
        WHERE Name in (?,?,?,?,?);
    """
    cursor_result.execute(sql_wins, winners)

    sql_old = """
        UPDATE Current_Game
        SET Active = 0
    """
    cursor_result.execute(sql_old)

    conn.commit()
    conn.close()

    await ctx.message.add_reaction(THUMBS_UP)
    await magic_internet_points(ctx)


@bot.command(name='isms', help='Add an "-ism" ("QUOTE" PERSON)')
async def add_ism(ctx, quote, person=None):
    author = ctx.author.display_name
    conn = connect_to_db()
    cursor = conn.cursor()

    sql = """
        INSERT INTO Isms (Person, Quote, Author)
        VALUES (?, ?, ?)
    """
    cursor.execute(sql, [person, quote, author])
    conn.commit()
    conn.close()
    await ctx.message.add_reaction(THUMBS_UP)


if __name__ == '__main__':
    bot.run(TOKEN)

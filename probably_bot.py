# bot.py
import os
import random

import discord
from discord.ext import commands
from dotenv import load_dotenv

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from table2ascii import table2ascii as t2a, PresetStyle


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
intents=discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']


@bot.command(name='customs', help='Creates 2 teams of 5')
async def customs(ctx):
    voice_state = ctx.author.voice

    if not voice_state:
        return
    
    member_names = [x.name for x in voice_state.channel.voice_members]
    members_count = len(member_names)

    if members_count < 10:
        await ctx.channel.send(f'LF{10 - members_count}M Gold-Plat elo Customs')
        return
    if members_count > 10:
        await ctx.channel.send('Too many niggas!')
        return
    
    random.shuffle(member_names)
    team_one = member_names[:members_count//2]
    team_two = member_names[members_count//2:]

    team_one_text = '\n'.join(team_one)
    team_two_text = '\n'.join(team_two)
    output = f'{get_intro(member_names)}\n>>> **Blue Team:**\n{team_one_text}\n\n--------------------\n\n**RedTeam:**\n{team_two_text}'

    await ctx.channel.send(f'''\n{output}\n''')


@bot.command(name='points', help='Displays Magic Internet Points')
async def magic_internet_points(ctx):
    creds = oauth()

    try:
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()
        ss_result = sheet.values().get(spreadsheetId='1V7ChDsT15t4PG_7WQ5jHO8il7FvT5w2hl5vrh7Hb1po', range="Sheet1").execute()
        rows = ss_result.get('values', [])

        if not rows:
            print('No data found.')
            return

        title= '*** Magic Internet Points ***'

        headers = []
        for header in rows.pop(0):
            headers.append(header)
        headers.append('Win Rate')

        rows.sort(key=lambda x: calc_win_rate(x[1], x[2]))
        rows.reverse()
        body = []
        for row in rows:
            name = row[0]
            wins = row[1]
            games = row[2]

            win_rate = calc_win_rate(wins, games)
            percent_string = '{:.2%}'.format(win_rate) if win_rate >= 0 else 'NEW'

            body.append([name, wins, games, percent_string])

        output = t2a(
            header=headers,
            body=body,
            style=PresetStyle.simple,
        )

        await ctx.send(f"```\n{title}\n\n{output}\n```")

    except HttpError as err:
        print(err)


@bot.command(name='win', help='Records winner of game')
async def win(ctx):
    creds = oauth()

    try:
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()
        ss_result = sheet.values().get(spreadsheetId='1V7ChDsT15t4PG_7WQ5jHO8il7FvT5w2hl5vrh7Hb1po', range="Sheet1").execute()
        rows = ss_result.get('values', [])

        if not rows:
            print('No data found.')
            return

        title= '*** Magic Internet Points ***'

        headers = []
        for header in rows.pop(0):
            headers.append(header)
        headers.append('Win Rate')

        rows.sort(key=lambda x: calc_win_rate(x[1], x[2]))
        rows.reverse()
        body = []
        for row in rows:
            name = row[0]
            wins = row[1]
            games = row[2]

            win_rate = calc_win_rate(wins, games)
            percent_string = '{:.2%}'.format(win_rate) if win_rate >= 0 else 'NEW'

            body.append([name, wins, games, percent_string])

        output = t2a(
            header=headers,
            body=body,
            style=PresetStyle.simple,
        )

        await ctx.send(f'"\nScore Recorded\n```\n{title}\n\n{output}\n```"')

    except HttpError as err:
        print(err)


def calc_win_rate(wins, games):
    wins = int(wins)
    games = int(games)
    if not games:
        return -1
    
    return wins/games


def get_intro(member_names):
    options = [
        'Probably Customs',
        'Get your Party Cardi!',
        'Put on your try-hard pants',
        "LET'S FUCKING GO!!!!!!!",
        'Come Get Some',
        'Bouta be a JUNGLE GAP',
        'Support is rrrrrrrrrRunning it down',
        'Forecasting a Flame Horizon',
        f'First Blood, 0:{random.choice(range(30, 60))}, bot river',
        f'First Blood, 1:{random.choice(range(0, 60))}, bot'
        f'First Blood: {random.choice(member_names)}',
        f'Target Ban Locked: {random.choice(member_names)}',
        f'WARNING! {random.choice(member_names)} Pop Off Incoming!',
        f"No {random.choice(member_names)}, don't do it to 'em.",
        'Ugh, go next...',
        f'Report {random.choice(member_names)}. Soft-inting.',
        "Fuck 'em up!",
        "Jungle ASol... you won't",
        'This is gonna be a baka-laka-ham-dak',
        'Turn these idiots into CONVERTIBLES',
        "Show 'em their shit don't fit in your pocket",
        'Put down the bananas so you can play the game.',
        f'{random.choice(range(5, 15))}. Mid 0 Vision Score',
        ]
    return random.choice(options)

def oauth():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return creds


if __name__ == '__main__':
    bot.run(TOKEN)
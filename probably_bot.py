# bot.py
import os
import random

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
intents=discord.Intents.all()

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command(name='customs', help='Creates 2 teams of 5')
async def customs(ctx):
    author = ctx.author
    voice_state = author.voice
    # if not voice_state:
    #     return
    # voice_channel = voice_state.channel
    # voice_members = voice_channel.members
    # member_names = [x.name for x in voice_members]
    member_names = list(str(x) for x in range(10))
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
    start_text = [
        'Probably Customs',
        'Get your Party Cardi!',
        'Put on your try-hard pants',
    ]
    team_one_text = '\n'.join(team_one)
    team_two_text = '\n'.join(team_two)
    response = '{}\n>>> **Blue Team:**\n{}\n\n--------------------\n\n**RedTeam:**\n{}'.format(random.choice(start_text), team_one_text, team_two_text)


    print(response)

    await ctx.channel.send(response)

    


bot.run(TOKEN)
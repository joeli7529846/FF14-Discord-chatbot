import discord
import pickle
from discord.ext import commands
import os
from dotenv import load_dotenv


class Cog_Extension(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        load_dotenv()
        self.TOKEN = os.getenv('DISCORD_TOKEN')
        self.GUILDID_TOKEN = os.getenv('GUILDID_TOKEN')
       
        
        
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
        #讀取字典
        with open("item_dict.pkl", "rb") as tf:
            self.item_dict = pickle.load(tf)
        self.wordlist = [word for word in self.item_dict]
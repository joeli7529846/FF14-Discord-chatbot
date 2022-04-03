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
        with open("item_dict1.pkl", "rb") as tf:
            self.item_dict1 = pickle.load(tf)
        print("item_dict1.pkl complete")
        with open("item_dict2.pkl", "rb") as tf:
            self.item_dict2 = pickle.load(tf)
        print("item_dict2.pkl complete")
        self.item_dict = {**self.item_dict1, **self.item_dict2}
        print("item_dict.pkl complete")
        
        self.wordlist = [word for word in self.item_dict]
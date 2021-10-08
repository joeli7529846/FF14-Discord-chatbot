#導入Discord.py
import discord
import difflib
from discord.ext import commands
from core.classes import Cog_Extension
from random import choice

class draw(Cog_Extension):
    @commands.command()
    
    async def draw(self,ctx):
        member_list = []
        async for user in ctx.guild.members():
            
            if str(user.status) != "offline":
                print(user)
                member_list.append(str(user))
        await ctx.message.reply(choice(member_list))
def setup(bot):
    bot.add_cog(draw(bot))
#導入Discord.py
import discord
import difflib
from discord.ext import commands
from core.classes import Cog_Extension
import numpy as np

class random_team(Cog_Extension):
    @commands.command()
    
    async def rteam(self,ctx):
        #獲取在線名單
        guild = self.bot.get_guild(int(self.GUILDID_TOKEN))
        member_list = []
        for user in guild.members:
            if str(user.status) != "offline":
                # print(user)
                member_list.append(f"{user.display_name}")
        
        raid_list = [4,8]
        # print(guild.members)
        #先抽副本人數
        member_count = list(np.random.choice(raid_list, size=1, replace=False, p=None))[0]
        #再抽參與人員名單
        team_list = list(np.random.choice(member_list, size=member_count, replace=False, p=None))

        if member_count == 4:
            embed=discord.Embed(title="四人副本", 
                                color=discord.Color.red())
            embed.add_field(name="MT", 
                            value=team_list[0], 
                            inline=False)
            embed.add_field(name="D1", 
                            value=team_list[1], 
                            inline=True)
            embed.add_field(name="D2", 
                            value=team_list[2], 
                            inline=True)
            embed.add_field(name="H1", 
                            value=team_list[3], 
                            inline=False)
        
        elif member_count == 8:
            embed=discord.Embed(title="八人副本", 
                                color=discord.Color.red())
            embed.add_field(name="MT", 
                            value=team_list[0], 
                            inline=True)
            embed.add_field(name="ST", 
                            value=team_list[1], 
                            inline=True)
            embed.add_field('\u200b', '\u200b')
            embed.add_field(name="D1", 
                            value=team_list[2], 
                            inline=True)
            embed.add_field(name="D2", 
                            value=team_list[3], 
                            inline=True)
            embed.add_field('\u200b', '\u200b')
            embed.add_field(name="D3", 
                            value=team_list[4], 
                            inline=True)
            
            embed.add_field(name="D4", 
                            value=team_list[5], 
                            inline=True)
            embed.add_field('\u200b', '\u200b')
            embed.add_field(name="H1", 
                            value=team_list[6], 
                            inline=True)
            embed.add_field(name="H2", 
                            value=team_list[7], 
                            inline=True)

        await ctx.message.reply(embed=embed)


def setup(bot):
    bot.add_cog(random_team(bot))
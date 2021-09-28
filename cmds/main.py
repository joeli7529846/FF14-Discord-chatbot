#導入Discord.py
import discord
import pandas as pd
import pickle
import difflib
from discord.ext import commands
from dotenv import load_dotenv
import os

class main(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        load_dotenv()
        self.TOKEN = os.getenv('DISCORD_TOKEN')
        self.GUILDID_TOKEN = int(os.getenv('GUILDID_TOKEN'))
        #讀取字典
        with open("item_dict.pkl", "rb") as tf:
            self.item_dict = pickle.load(tf)
        self.wordlist = [word for word in self.item_dict]
    
    @commands.command()
    async def ping(self,ctx):
        await ctx.send('Pong!')

    #調用event函式庫
    @commands.Cog.listener()
    #當機器人完成啟動時
    async def on_ready(self):
        print('目前登入身份：',self.bot.user)

    
    #新成員加入
    @commands.Cog.listener()
    #當有訊息時
    async def on_member_join(self,member):
        guild = self.bot.get_guild(self.GUILDID_TOKEN)
        for channel in guild.channels:
            if channel.name == '一般':#<<記得改"一般"
                await channel.send(f"<@{member.id}> 你好呀:sunglasses:  請輸入你的遊戲ID，管理員看到就會把你加進公會~")


    @commands.Cog.listener()
    #當有訊息時
    async def on_message(self,message):
        embed = discord.Embed()
        #排除自己的訊息，避免陷入無限循環
        if message.author == self.bot.user:
            return
                
        #翻譯
        if message.content.startswith('?tr '):
            user_word = message.content.replace('?tr ',"")
            user_word = user_word.lstrip().rstrip()
            
            if user_word in self.item_dict:
                
                if "簡體中文" in self.item_dict[user_word]:
                    
                    
                    user_wordlist = [f"{key} : {value}" for key,value in self.item_dict[user_word].items()]+[f"[詳細資訊連結](https://ff14.huijiwiki.com/wiki/%E7%89%A9%E5%93%81:{self.item_dict[user_word]['簡體中文']})"]
                    
                    embed.description = "\n".join(user_wordlist)
                    embed.set_thumbnail(url = f"https://universalis-ffxiv.github.io/universalis-assets/icon2x/{self.item_dict[user_word]['ID']}.png")
                    await message.reply(embed=embed, mention_author=True)
                    # await message.channel.send(embed=embed)
                    
                else:
                    user_wordlist = [f"{key} : {value}" for key,value in self.item_dict[user_word].items()]+[f"[詳細資訊連結](https://ff14.huijiwiki.com/wiki/%E7%89%A9%E5%93%81:{user_word})"]
                    embed.description = "\n".join(user_wordlist)
                    embed.set_thumbnail(url = f"https://universalis-ffxiv.github.io/universalis-assets/icon2x/{self.item_dict[user_word]['ID']}.png")
                    await message.reply(embed=embed, mention_author=True)

                    # await message.channel.send(embed=embed)
                    
            else:
                wordsim_list = difflib.get_close_matches(user_word,self.wordlist,10,cutoff=0.1)
                
                if len(wordsim_list) > 0:
                    embed.description ="你可能要查詢的詞:\n"+"\n".join(wordsim_list)
                    await message.channel.send(embed=embed)
                else:
                    await message.channel.send("無相關資訊")

        #查市價
        elif message.content.startswith('?bs '):
            user_word = message.content.replace('?bs ',"")
            user_word = user_word.lstrip().rstrip()
            if user_word in self.item_dict:
                if "ID" in self.item_dict[user_word]:
                    embed.description = f"[{user_word}價格網址](https://universalis.app/market/{self.item_dict[user_word]['ID']})"
                    embed.set_thumbnail(url = f"https://universalis-ffxiv.github.io/universalis-assets/icon2x/{self.item_dict[user_word]['ID']}.png")
                    await message.reply(embed=embed, mention_author=True)

                else:
                    embed.description = f"[{user_word}價格網址](https://universalis.app/market/{user_word})"
                    embed.set_thumbnail(url = f"https://universalis-ffxiv.github.io/universalis-assets/icon2x/{self.item_dict[user_word]['ID']}.png")
                    await message.reply(embed=embed, mention_author=True)

            else:
                wordsim_list = difflib.get_close_matches(user_word,self.wordlist,10,cutoff=0.1)
                if len(wordsim_list) > 0:
                    embed.description ="你可能要查詢的詞:\n"+"\n".join(wordsim_list)
                    
                    await message.reply(embed=embed, mention_author=True)

                else:
                    await message.reply("無相關資訊")

       

def setup(bot):
    bot.add_cog(main(bot))


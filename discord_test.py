#導入Discord.py
import discord
import requests
import pandas as pd
import pickle
import difflib
from discord.ext import commands
import ahocorasick
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import chardet
# def build_actree(wordlist):
#     actree = ahocorasick.Automaton()
#     for index,word in enumerate(wordlist):
#         actree.add_word(str(word), (index, str(word)))
#     actree.make_automaton()
#     return actree

def build_actree(wordlist):
    actree = ahocorasick.Automaton()
    for index,word in enumerate(wordlist):
        actree.add_word(str(word), (index, str(word)))
    actree.make_automaton()
    return actree

if __name__ == '__main__':

    header = {"user-agent": "Mozilla/5.0 ((Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"}
    #存放灰機WIKI
    basequestion_list = ["籌備","晋升","復興","魂武","元靈","老主顧"]
    base_knowledge = {"籌備":"筹备军需品列表","晋升":"大国防联军","復興":"重建伊修加德","魂武":"元灵武器","元靈":"元灵武器","老主顧":"老主顾交易"}
    #讀取Token
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    GUILDID_TOKEN = os.getenv('GUILDID_TOKEN')
    
    #讀取字典
    with open("item_dict.pkl", "rb") as tf:
        item_dict = pickle.load(tf)

    wordlist = [word for word in item_dict]
    

    
    #client是我們與Discord連結的橋樑
    #client = discord.Client()
    intents = discord.Intents.default()
    intents.members = True
    client = discord.Client(intents=intents)
    # client = commands.Bot(command_prefix='.',intents =intents)
    
    # bot = discord.ext.commands.Bot(command_prefix = "your_prefix")

    

    #調用event函式庫
    @client.event
    #當機器人完成啟動時
    async def on_ready():
        print('目前登入身份：',client.user)

    
    #新成員加入
    @client.event
    #當有訊息時
    async def on_member_join(member):
        guild = client.get_guild(GUILDID_TOKEN)
        
        for channel in guild.channels:
        
            if channel.name == '一般':#<<記得改"一般"
                await channel.send(f"<@{member.id}> 你好呀:sunglasses:  請輸入你的遊戲ID，管理員看到就會把你加進公會~")
        



    @client.event
    #當有訊息時
    async def on_message(message):
        embed = discord.Embed()
        #排除自己的訊息，避免陷入無限循環
        if message.author == client.user:
            return
                
        # if message.type is discord.MessageType.new_member and message.guild.id == id:
        #     embed = discord.Embed(description=f"@{message.author.mention} 你好呀=w= 請輸入你的遊戲ID，管理員看到就會把你加進公會~")
        #     log_channel = message.guild.get_channel(id)
        #     await log_channel.send(embed=embed)

        #翻譯
        if message.content.startswith('?tr '):
            user_word = message.content.replace('?tr ',"")
            user_word = user_word.lstrip().rstrip()
            
            if user_word in item_dict:
                
                if "簡體中文" in item_dict[user_word]:
                    
                    
                    user_wordlist = [f"{key} : {value}" for key,value in item_dict[user_word].items()]+[f"[詳細資訊連結](https://ff14.huijiwiki.com/wiki/%E7%89%A9%E5%93%81:{item_dict[user_word]['簡體中文']})"]
                    
                    embed.description = "\n".join(user_wordlist)
                    embed.set_thumbnail(url = f"https://universalis-ffxiv.github.io/universalis-assets/icon2x/{item_dict[user_word]['ID']}.png")
                    await message.reply(embed=embed, mention_author=True)
                    # await message.channel.send(embed=embed)
                    
                else:
                    user_wordlist = [f"{key} : {value}" for key,value in item_dict[user_word].items()]+[f"[詳細資訊連結](https://ff14.huijiwiki.com/wiki/%E7%89%A9%E5%93%81:{user_word})"]
                    embed.description = "\n".join(user_wordlist)
                    embed.set_thumbnail(url = f"https://universalis-ffxiv.github.io/universalis-assets/icon2x/{item_dict[user_word]['ID']}.png")
                    await message.reply(embed=embed, mention_author=True)

                    # await message.channel.send(embed=embed)
                    
            else:
                wordsim_list = difflib.get_close_matches(user_word,wordlist,10,cutoff=0.1)
                
                if len(wordsim_list) > 0:
                    embed.description ="你可能要查詢的詞:\n"+"\n".join(wordsim_list)
                    await message.channel.send(embed=embed)
                else:
                    await message.channel.send("無相關資訊")

        #查市價
        elif message.content.startswith('?bs '):
            user_word = message.content.replace('?bs ',"")
            user_word = user_word.lstrip().rstrip()
            if user_word in item_dict:
                if "ID" in item_dict[user_word]:
                    embed.description = f"[{user_word}價格網址](https://universalis.app/market/{item_dict[user_word]['ID']})"
                    embed.set_thumbnail(url = f"https://universalis-ffxiv.github.io/universalis-assets/icon2x/{item_dict[user_word]['ID']}.png")
                    await message.reply(embed=embed, mention_author=True)

                else:
                    embed.description = f"[{user_word}價格網址](https://universalis.app/market/{user_word})"
                    embed.set_thumbnail(url = f"https://universalis-ffxiv.github.io/universalis-assets/icon2x/{item_dict[user_word]['ID']}.png")
                    await message.reply(embed=embed, mention_author=True)

            else:
                wordsim_list = difflib.get_close_matches(user_word,wordlist,10,cutoff=0.1)
                if len(wordsim_list) > 0:
                    embed.description ="你可能要查詢的詞:\n"+"\n".join(wordsim_list)
                    
                    await message.reply(embed=embed, mention_author=True)

                else:
                    await message.reply("無相關資訊")

        elif message.content.startswith('請問'):
            user_word = message.content.replace('請問',"")
            actree = build_actree(wordlist=basequestion_list)
            send_list = [i[1][1] for i in actree.iter(user_word)]
            if len(send_list) == 1:
                wiki_url = f"https://ff14.huijiwiki.com/wiki/{base_knowledge[send_list[0]]}"
                await message.reply(f"這篇可以參考看看~\n{wiki_url}", mention_author=True)
            # elif len(send_list) == 0:



        

    client.run(TOKEN) #TOKEN 在剛剛 Discord Developer 那邊「BOT」頁面裡面
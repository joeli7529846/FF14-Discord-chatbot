from time import sleep, time
import pandas as pd
from discord.ext import commands,tasks
from core.classes import Cog_Extension
import discord
import pygsheets
import difflib
from random import choice
import numpy as np
import math
from discord_components import DiscordComponents, Button, ButtonStyle
import asyncio

class ask(Cog_Extension):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        # self.read_gsheet.start()
        DiscordComponents(self.bot)
        ask.read_gsheet(self).start()
        self.idn=["https://i.imgur.com/M9hQgZC.gif",
                  "https://i.imgur.com/2VXiwMW.jpg",
                  "https://i.imgur.com/dAV35RN.jpg",
                  "https://i.imgur.com/cd4v2yA.jpg",
                  "https://i.imgur.com/YvMmcBf.jpg",
                  "http://i.imgur.com/DJ8lE9L.jpg",
                  "https://i.imgur.com/FeVL45J.jpg",
                  "https://i.imgur.com/37u7gfR.gif",
                  "https://i.imgur.com/WtYPzMt.png",
                  "http://i.imgur.com/7Za5hZA.jpg",
                  "https://i.imgur.com/BtVDnpT.jpg",
                  "https://i.imgur.com/TSfPO49.jpg",
                  "http://i.imgur.com/RecpaoD.jpg"]
    
    @tasks.loop(minutes = 5)
    async def read_gsheet(self):
        
        gc =  pygsheets.authorize(service_account_file='google_apikey.json')

        survey_url = 'https://docs.google.com/spreadsheets/d/1C62JiqFM-KPMlwTwFCaH1qutYOexXRo-dxPmtBidfJ0/edit#gid=0'
        sh =  gc.open_by_url(survey_url)

        ws =  sh.worksheet_by_title('FF14 QA')

        df =  ws.get_as_df(has_header=True,empty_value='', include_tailing_empty=True,numerize=False)
        #df 存成字典格式
        qa_dict =   pd.Series(df.answer.values,index=df.question).to_dict()
        question_list =  df["question"].tolist()
        #讀取成員資訊
        ws =  sh.worksheet_by_title('成員資訊卡片')

        info_df =  ws.get_as_df(has_header=True,empty_value='', include_tailing_empty=True,numerize=False)
        name_list = info_df["名稱"].tolist()
        info_dict={}
        for index,row in info_df.iterrows():
            
            info_dict[row["名稱"]]={"職業":row["職業"],
                                    "出沒地點":row["出沒地點"],
                                    "攻擊":row["攻擊"],
                                    "防禦":row["防禦"],
                                    "防禦":row["防禦"],
                                    "色色":row["色色"],
                                    "介紹":row["介紹"],
                                    "頭像":row["頭像"],
                                    }
            
        return self.qa_dict,self.question_list,self.info_dict,self.name_list
            
    @commands.command()
    #當有訊息時
    async def info(self,ctx):
        embed = discord.Embed()
        word = ctx.message.content.replace("/info ","")
        
        #搜尋名稱
        wordsim_list = difflib.get_close_matches(word,self.name_list,50,cutoff=0.4)
        if len(wordsim_list) == 1:
            embed=discord.Embed(title=word, 
                        color=discord.Color.gold())
            embed.add_field(name="職業", 
                    value=self.info_dict[word]["職業"], 
                    inline=False)
            embed.add_field(name="攻擊", 
                    value=self.info_dict[word]["攻擊"], 
                    inline=True)
            embed.add_field(name="防禦", 
                    value=self.info_dict[word]["防禦"], 
                    inline=True)
            embed.add_field(name="色色", 
                    value=self.info_dict[word]["色色"], 
                    inline=True)
            embed.add_field(name="出沒地點", 
                    value=self.info_dict[word]["出沒地點"], 
                    inline=False)
            embed.add_field(name="介紹", 
                    value=self.info_dict[word]["介紹"], 
                    inline=False)
            
            embed.set_thumbnail(url = self.info_dict[word]["頭像"])
            
            
            await ctx.message.reply(embed=embed, mention_author=True)
        
        elif len(wordsim_list) > 1:
            embed.description ="你可能要查詢的名片:\n"+"\n".join(wordsim_list)
            await ctx.message.reply(embed=embed, mention_author=True)
            
    
    
    @commands.command()
    #當有訊息時
    async def ask(self,ctx):
        embed = discord.Embed()
        word = ctx.message.content.replace("/ask ","")
        
        #先從questionlist搜尋相似的問題
        wordsim_list = difflib.get_close_matches(word,self.question_list,50,cutoff=0.2)
        if len(wordsim_list) == 1:
            embed.description = self.qa_dict[wordsim_list[0]]
            if "macro" in wordsim_list[0]:
                await ctx.message.reply(embed=embed, mention_author=True)
            else:
                await ctx.message.reply(self.qa_dict[wordsim_list[0]], mention_author=True)
        elif len(wordsim_list) > 1:
            
            if word in wordsim_list:
                
                embed.description = self.qa_dict[wordsim_list[0]]
                if "macro" in wordsim_list[0]:
                    await ctx.message.reply(embed=embed, mention_author=True)
                else:
                    await ctx.message.reply(self.qa_dict[wordsim_list[0]], mention_author=True)
            else:
                
                page_num = math.ceil(len(wordsim_list)/5) 
                if len(wordsim_list) > 5:
                    # print(len(wordsim_list))
                    #建立每頁的embed
                    #wordsim_list分割page
                    pages_list = np.array_split(wordsim_list, page_num)
                    paginationList = []
                    for page_list in pages_list:
                        page = discord.Embed (
                            title = '你可能要查詢的詞',
                            description = "\n".join(page_list),
                            colour = discord.Colour.orange()
                        )
                        paginationList.append(page)
                    current = 0
                    #Sending first message
                    #I used ctx.reply, you can use simply send as well
                    mainMessage = await ctx.reply(
                        embed = paginationList[current],
                        components = [ #Use any button style you wish to :)
                            [
                                Button(
                                    label = "Prev",
                                    id = "back",
                                    style = ButtonStyle.red
                                ),
                                Button(
                                    label = f"Page {int(paginationList.index(paginationList[current])) + 1}/{len(paginationList)}",
                                    id = "cur",
                                    style = ButtonStyle.grey,
                                    disabled = True
                                ),
                                Button(
                                    label = "Next",
                                    id = "front",
                                    style = ButtonStyle.red
                                )
                            ]
                        ]
                    )
                    #Infinite loop
                    while True:
                        #Try and except blocks to catch timeout and break
                        try:
                            interaction = await self.bot.wait_for(
                                "button_click",
                                check = lambda i: i.component.id in ["back", "front"], #You can add more
                                timeout = 18.0 #10 seconds of inactivity
                            )
                            #Getting the right list index
                            if interaction.component.id == "back":
                                current -= 1
                            elif interaction.component.id == "front":
                                current += 1
                            #If its out of index, go back to start / end
                            if current == len(paginationList):
                                current = 0
                            elif current < 0:
                                current = len(paginationList) - 1

                            #Edit to new page + the center counter changes
                            await interaction.respond(
                                type = 7,
                                embed = paginationList[current],
                                components = [ #Use any button style you wish to :)
                                    [
                                        Button(
                                            label = "Prev",
                                            id = "back",
                                            style = ButtonStyle.red
                                        ),
                                        Button(
                                            label = f"Page {int(paginationList.index(paginationList[current])) + 1}/{len(paginationList)}",
                                            id = "cur",
                                            style = ButtonStyle.grey,
                                            disabled = True
                                        ),
                                        Button(
                                            label = "Next",
                                            id = "front",
                                            style = ButtonStyle.red
                                        )
                                    ]
                                ]
                            )
                        except asyncio.TimeoutError:
                            #Disable and get outta here
                            await mainMessage.edit(
                                components = [
                                    [
                                        Button(
                                            label = "Prev",
                                            id = "back",
                                            style = ButtonStyle.red,
                                            disabled = True
                                        ),
                                        Button(
                                            label = f"Page {int(paginationList.index(paginationList[current])) + 1}/{len(paginationList)}",
                                            id = "cur",
                                            style = ButtonStyle.grey,
                                            disabled = True
                                        ),
                                        Button(
                                            label = "Next",
                                            id = "front",
                                            style = ButtonStyle.red,
                                            disabled = True
                                        )
                                    ]
                                ]
                            )
                            break  

                else:
                    embed.description ="你可能要查詢的詞:\n"+"\n".join(wordsim_list)
                    await ctx.message.reply(embed=embed, mention_author=True)
        else:
            await ctx.message.reply(choice(self.idn))
        
        


def setup(bot):
    bot.add_cog(ask(bot))
import pandas as pd
from discord.ext import commands
from core.classes import Cog_Extension
import discord
import pygsheets
import difflib
from random import choice
class ask(Cog_Extension):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.qa_dict,self.question_list = ask.read_gsheet(self)
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
    
    def read_gsheet(self):
        gc = pygsheets.authorize(service_account_file='google_apikey.json')

        survey_url = 'https://docs.google.com/spreadsheets/d/1C62JiqFM-KPMlwTwFCaH1qutYOexXRo-dxPmtBidfJ0/edit#gid=0'
        sh = gc.open_by_url(survey_url)

        ws = sh.worksheet_by_title('FF14 QA')

        df = ws.get_as_df(empty_value='', include_tailing_empty=False)
        #df 存成字典格式
        qa_dict = pd.Series(df.answer.values,index=df.question).to_dict()
        question_list = df["question"].tolist()
        

        return qa_dict,question_list
    
    
    @commands.command()
    #當有訊息時
    async def ask(self,ctx):
        embed = discord.Embed()
        
        
        #先從questionlist搜尋相似的問題
        wordsim_list = difflib.get_close_matches(ctx.message.content,self.question_list,5,cutoff=0.2)
        if len(wordsim_list) == 1:
            embed.description = self.qa_dict[wordsim_list[0]]
            if "macro" in wordsim_list[0]:
                await ctx.message.reply(embed=embed, mention_author=True)
            else:
                await ctx.message.reply(self.qa_dict[wordsim_list[0]], mention_author=True)
        elif len(wordsim_list) > 1:
            print(ctx.message.content)
            if ctx.message.content in wordsim_list:
                print(ctx.message.content)
                embed.description = self.qa_dict[wordsim_list[0]]
                if "macro" in wordsim_list[0]:
                    await ctx.message.reply(embed=embed, mention_author=True)
                else:
                    await ctx.message.reply(self.qa_dict[wordsim_list[0]], mention_author=True)
            else:
                embed.description ="你可能要查詢的詞:\n"+"\n".join(wordsim_list)
                await ctx.message.reply(embed=embed, mention_author=True)
        else:
            await ctx.message.reply(choice(self.idn))
        
        


def setup(bot):
    bot.add_cog(ask(bot))
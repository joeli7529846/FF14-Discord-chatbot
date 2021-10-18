import pandas as pd
from discord.ext import commands
from core.classes import Cog_Extension
import discord
import pygsheets
import difflib

class ask(Cog_Extension):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.qa_dict,self.question_list = ask.read_gsheet(self)
        
    
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
        wordsim_list = difflib.get_close_matches(ctx.message.content,self.question_list,5,cutoff=0.5)
        if len(wordsim_list) == 1:
            embed.description = self.qa_dict[wordsim_list[0]]
            if "http" in ctx.message.content:
                await ctx.message.reply(self.qa_dict[wordsim_list[0]], mention_author=True)
            await ctx.message.reply(embed=embed, mention_author=True)
        elif len(wordsim_list) > 1:
            embed.description ="你可能要查詢的詞:\n"+"\n".join(wordsim_list)
            await ctx.message.reply(embed=embed, mention_author=True)
        else:
            await ctx.message.reply("窩不知道")
        
        


def setup(bot):
    bot.add_cog(ask(bot))
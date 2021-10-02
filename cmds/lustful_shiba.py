import pandas as pd
from discord.ext import commands
from core.classes import Cog_Extension
import discord
from random import choice
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
from scipy.linalg import norm
class main(Cog_Extension):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.table=[]
        self.nohokh = ["https://i.imgur.com/cZksr04.jpg","https://i.imgur.com/wH4CJLF.jpg","https://i.imgur.com/ag0DVMT.jpg"]
    
    def tf_similarity(self,s1, s2):
        def add_space(s):
            return ' '.join(list(s))

        # 將字中間加入空格
        s1, s2 = add_space(s1), add_space(s2)
        # 轉化為TF矩陣
        cv = CountVectorizer(tokenizer=lambda s: s.split())
        corpus = [s1, s2]
        vectors = cv.fit_transform(corpus).toarray()
        # 計算TF係數
        return np.dot(vectors[0], vectors[1]) / (norm(vectors[0]) * norm(vectors[1]))
    
    
    
    @commands.Cog.listener()
    #當有訊息時
    async def on_message(self,message):
        embed = discord.Embed()
        #排除自己的訊息，避免陷入無限循環
        if message.author == self.bot.user:
            return
        
        # #講出字串含有兩個色字的人送往可以色色頻道
        # if message.content.count('色') == 2:
        #     # channel = discord.utils.get(893154759844986931, name = f"{message.author}'s channel")
        #     await self.bot.move_member(message.author,893154759844986931)

        noh_sim = self.tf_similarity(message.content, "不可以色色")
        okh_sim = self.tf_similarity(message.content, "可以色色")
        print(noh_sim)
        print(okh_sim)
        #不可以色色排組對應圖片
        if noh_sim > 0.7 and noh_sim > okh_sim:
            if "可以色色" and "不可以色色" in self.table:
                self.table=[]
                await message.reply(choice(self.nohokh))#特招
            else:
                noh = ["https://imgur.dcard.tw/TUGMyF7h.jpg","https://imgur.dcard.tw/ZayW5My.jpg","https://i.imgur.com/WLbQBlT.jpg","https://i.imgur.com/nGI4pbO.jpg","https://i.imgur.com/jrOvlgH.jpg","https://i.imgur.com/68mqoce.jpg"]
                self.table.append("不可以色色")
                await message.reply(choice(noh))#不可以色色康特
            # await message.channel.send(embed=embed)
        elif okh_sim > 0.7 and noh_sim < okh_sim:
            if "可以色色" and "不可以色色" in self.table:
                self.table=[]
                await message.reply(choice(self.nohokh))#特招
            else:
                okh = ["https://i.imgur.com/UVZti2m.jpg","https://i.imgur.com/FoGDvP7.jpg","https://i.imgur.com/c2pDzLJ.jpg","https://i.imgur.com/0Ux7atA.jpg","https://i.imgur.com/hnnSpzr.jpg","https://i.imgur.com/F03Raad.jpg"]
                self.table.append("可以色色")
                await message.reply(choice(okh))#可以色色康特
        


def setup(bot):
    bot.add_cog(main(bot))
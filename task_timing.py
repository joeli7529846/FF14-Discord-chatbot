import pandas as pd
from discord.ext import commands,tasks
from core.classes import Cog_Extension
import discord
import json,asyncio,datetime
from datetime import datetime,timezone,timedelta

class tasktiming(Cog_Extension):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.tasktime.start()
        self.count=0
        self.id = 0
        
    
    @tasks.loop(seconds=10)
    async def tasktime(self):
        embed = discord.Embed()
        self.generalchannel = self.bot.get_channel(779782707080069193)#記得改成功會generalID
        
        self.channel = self.bot.get_channel(887264861510328340)#記得改糾團頻道ID
        #由於伺服器架在美國所以要轉時區
        now_time = datetime.utcnow().replace(tzinfo=timezone.utc)
        now_time = now_time.astimezone(timezone(timedelta(hours=8)))
        now_time = now_time.strftime('%m/%d-%H:%M')
        # print(now_time)
        with open("setting.json",'r',encoding="utf8") as jfile:
            jdata = json.load(jfile)
        # print(len(jdata))
        if len(jdata) >0:
            #遍例每筆資料確認每筆時間
            for key in list(jdata):
                
                # print(key, ":", jdata[key])
                if datetime.strptime(now_time, '%m/%d-%H:%M') < datetime.strptime(jdata[key]["time"], '%m/%d-%H:%M'):
                    remain_hour = datetime.strptime(jdata[key]["time"], '%m/%d-%H:%M')-datetime.strptime(now_time, '%m/%d-%H:%M')
                    remain_hour = remain_hour.seconds/3600#轉成小時
                    # print(remain_hour)
                    #剩餘時間小於一小時執行下面動作
                    if remain_hour < 1 :
                        print("complete")
                        #在general頻道發通知
                        user_wordlist = ["有任務快開始囉~趕快來參加",f'任務名稱 : {jdata[key]["task"]}']+[f'時間 : {jdata[key]["time"]}']+[f'條件 : {jdata[key]["condition"]}' if "condition" in jdata[key] else '條件 : 無']+[f'[傳送門]( {jdata[key]["url"]})']
                    
                        embed.description = "\n".join(user_wordlist)
                        await self.generalchannel.send(embed=embed)
                        self.count=1
                        del jdata[key]
                        with open("setting.json",'w',encoding="utf8") as jfile:
                            jdata = json.dump(jdata,jfile,indent=4)
                        
                    else:
                        
                        pass
                else:
                    del jdata[key]
                    with open("setting.json",'w',encoding="utf8") as jfile:
                            jdata = json.dump(jdata,jfile,indent=4)
                    
    
        

    @commands.command()
    #當有訊息時
    async def set_channel(self,ctx,ch:int):
        self.channel = self.bot.get_channel(ch)
        await ctx.send(f"set channel:{self.channel.mention}")



    @commands.command()
    #訊息範本 : task 藏寶圖G12 主線5.0有80等腳色 10/2-20:00
    async def task(self,ctx):
        self.count = 0
        

        with open("setting.json",'r',encoding="utf8") as jfile:
            jdata = json.load(jfile)
        while str(self.id) in jdata:
            self.id = int(self.id)
            self.id += 1
            self.id = str(self.id)
        #拆解訊息
        # print(task)
        # print(condition)
        self.id = str(self.id)
        
        message_list = ctx.message.content.split()
        print(message_list)
        if message_list[0] != "task":
            await ctx.send(f"格式輸入錯誤~\n參考指令範本: task 任務名稱 條件 10/2-20:00")
        if len(message_list) == 4:
            task_info = {self.id:{"task":message_list[1],"condition":message_list[2],"time":message_list[-1],"url":ctx.message.jump_url}}
            jdata.update(task_info)
            
            with open("setting.json",'w',encoding="utf8") as jfile:
                jdata = json.dump(jdata,jfile,indent=4)
        elif len(message_list) == 3:
            task_info = {self.id:{"task":message_list[1],"time":message_list[-1],"url":ctx.message.jump_url}}
            jdata.update(task_info)
            
            with open("setting.json",'w',encoding="utf8") as jfile:
                jdata = json.dump(jdata,jfile,indent=4)
        else:
            await ctx.send(f"格式輸入錯誤~\n參考指令範本: task 任務名稱 條件 10/2-20:00")
        
        
        

        
        
        

def setup(bot):
    bot.add_cog(tasktiming(bot))
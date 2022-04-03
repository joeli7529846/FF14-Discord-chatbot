#導入Discord.py
import discord
import difflib
from discord.ext import commands
from core.classes import Cog_Extension
import asyncio
import pickle
class main(Cog_Extension):
    

    #調用event函式庫
    @commands.Cog.listener()
    #當機器人完成啟動時
    async def on_ready(self):
        bot_channel = self.bot.get_channel(int(780753727418138635))
        print('目前登入身份：',self.bot.user)
        # await bot_channel.send(f"我回來惹(*´∀`*)")

    
    
    @commands.command(aliases=["quit"])
    @commands.has_permissions(administrator=True)
    async def close(self,ctx):
        bot_channel = self.bot.get_channel(int(780753727418138635))
        await bot_channel.send(f"開發者把我關掉了，請稍後QQ")
        await self.bot.close()
        
    
    #新成員加入
    @commands.Cog.listener()
    #當有訊息時
    async def on_member_join(self,member):
        channel = self.bot.get_channel(int(779782707080069193))
        await channel.send(f"<@{member.id}> 你好呀:sunglasses:  請輸入你的遊戲ID，管理員看到就會把你加進公會~")

    

    @commands.Cog.listener()
    #當有訊息時
    async def on_message(self,message):
        embed = discord.Embed()
        pic_ext = ['.jpg','.png','.jpeg','.gif']
        with open("item_dict.pkl", "rb") as tf:
            self.item_dict = pickle.load(tf)
        self.wordlist = [word for word in self.item_dict]
        print("item_dict.pkl complete")
        #排除自己的訊息，避免陷入無限循環
        if message.author == self.bot.user:
            return
        # print(message.channel.id)
        if message.channel.id == int(912076442500755556):
            if len(message.attachments) > 0: #Checks if there are attachments
                for file in message.attachments:
                    if file.filename[-4:] not in pic_ext:
                        await asyncio.sleep(2)
                        await message.delete()
                    
            else:
                pic_count = 0
                for pic in pic_ext:
                    if pic in message.content:
                        pic_count+=1

                if pic_count == 0:
                    await asyncio.sleep(2)
                    await message.delete()

        #翻譯
        if message.content.startswith('?tr '):
            user_word = message.content.replace('?tr ',"")
            user_word = user_word.lstrip().rstrip()
            
            if user_word in self.item_dict:
                embed=discord.Embed(title=user_word, 
                                color=discord.Color.blue())
                    
                embed.add_field(name="各國翻譯", 
                        value="\n".join(self.item_dict[user_word]['各國翻譯']), 
                        inline=False)
                if "中文wiki" in self.item_dict[user_word]:
                    embed.add_field(name="中文wiki", 
                            value=self.item_dict[user_word]['中文wiki'], 
                            inline=True)
                if "英文wiki" in self.item_dict[user_word]:
                    embed.add_field(name="中文wiki", 
                            value=self.item_dict[user_word]['中文wiki'], 
                            inline=True)
                embed.add_field(name="拍賣價格", 
                        value="\n".join(self.item_dict[user_word]['拍賣價格']), 
                        inline=False)
                    
                embed.set_thumbnail(url = f"https://universalis-ffxiv.github.io/universalis-assets/icon2x/{self.item_dict[user_word]['ID']}.png")
                await message.reply(embed=embed, mention_author=True)
                # await message.channel.send(embed=embed)
                
 
                    
            else:
                wordsim_list = difflib.get_close_matches(user_word,self.wordlist,10,cutoff=0.1)
                
                if len(wordsim_list) > 0:
                    embed.description ="你可能要查詢的詞:\n"+"\n".join(wordsim_list)
                    await message.reply(embed=embed,delete_after=15)
                    await asyncio.sleep(15)
                    await message.delete()
                else:
                    await message.channel.send("無相關資訊")


       

def setup(bot):
    bot.add_cog(main(bot))


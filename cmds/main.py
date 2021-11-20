#導入Discord.py
import discord
import difflib
from discord.ext import commands
from core.classes import Cog_Extension


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
        #排除自己的訊息，避免陷入無限循環
        if message.author == self.bot.user:
            return
                
        #翻譯
        if message.content.startswith('?tr '):
            user_word = message.content.replace('?tr ',"")
            user_word = user_word.lstrip().rstrip()
            
            if user_word in self.item_dict:
                
                if "簡體中文" in self.item_dict[user_word]:
                    print(self.item_dict[user_word])
                    user_wordlist = [f"{key} : {value}" for key,value in self.item_dict[user_word].items()]
                    if "ID" in self.item_dict[user_word]:
                        bs_str = f"[價格網址](https://universalis.app/market/{self.item_dict[user_word]['ID']})"
                    else:
                        bs_str = "無拍賣資訊"
                    embed=discord.Embed(title=user_word, 
                                color=discord.Color.blue())
                    
                    embed.add_field(name="各國翻譯", 
                            value="\n".join(user_wordlist), 
                            inline=False)
                    embed.add_field(name="中文wiki", 
                            value=f"[詳細資訊連結](https://ff14.huijiwiki.com/wiki/%E7%89%A9%E5%93%81:{self.item_dict[user_word]['簡體中文']})", 
                            inline=True)
                    
                    embed.add_field(name="英文wiki", 
                            value=f"[詳細資訊連結](https://ffxiv.gamerescape.com/wiki/{self.item_dict[user_word]['英文'].replace(' ','_')})", 
                            inline=True)
                    embed.add_field(name="拍賣價格", 
                            value=bs_str, 
                            inline=False)
                    
                    embed.set_thumbnail(url = f"https://universalis-ffxiv.github.io/universalis-assets/icon2x/{self.item_dict[user_word]['ID']}.png")
                    await message.reply(embed=embed, mention_author=True)
                    # await message.channel.send(embed=embed)
                
                
                else:
                    user_wordlist = [f"{key} : {value}" for key,value in self.item_dict[user_word].items()]
                    if "ID" in self.item_dict[user_word]:
                        bs_str = f"[價格網址](https://universalis.app/market/{self.item_dict[user_word]['ID']})"
                    else:
                        bs_str = "無拍賣資訊"
                    embed=discord.Embed(title=user_word, 
                                color=discord.Color.blue())
                    embed.add_field(name="各國翻譯", 
                            value="\n".join(user_wordlist), 
                            inline=False)
                    embed.add_field(name="中文wiki", 
                            value=f"[詳細資訊連結](https://ff14.huijiwiki.com/wiki/%E7%89%A9%E5%93%81:{user_word})", 
                            inline=True)
                    embed.add_field(name="英文wiki", 
                            value=f"[詳細資訊連結](https://ffxiv.gamerescape.com/wiki/{self.item_dict[user_word]['英文'].replace(' ','_')})", 
                            inline=True)
                    embed.add_field(name="拍賣價格", 
                            value=bs_str, 
                            inline=False)
                    
                    embed.set_thumbnail(url = f"https://universalis-ffxiv.github.io/universalis-assets/icon2x/{self.item_dict[user_word]['ID']}.png")
                    await message.reply(embed=embed, mention_author=True)
                    
            else:
                wordsim_list = difflib.get_close_matches(user_word,self.wordlist,10,cutoff=0.1)
                
                if len(wordsim_list) > 0:
                    embed.description ="你可能要查詢的詞:\n"+"\n".join(wordsim_list)
                    await message.channel.send(embed=embed)
                else:
                    await message.channel.send("無相關資訊")


       

def setup(bot):
    bot.add_cog(main(bot))


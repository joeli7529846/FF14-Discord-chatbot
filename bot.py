import discord
from discord.ext import commands
from dotenv import load_dotenv
import os


if __name__ == '__main__':

    intents = discord.Intents.default()
    intents.members = True
    bot = commands.Bot(command_prefix='/',intents =intents)

    #讀取Token
    load_dotenv(dotenv_path="token.env")
    TOKEN = os.getenv('DISCORD_TOKEN')
    GUILDID_TOKEN = os.getenv('GUILDID_TOKEN')
    
    @bot.command()
    async def load(ctx,extension):
        bot.load_extension(f"cmds.{extension}")

    @bot.command()
    async def unload(ctx,extension):
        bot.unload_extension(f"cmds.{extension}")
    
    # bot.get_cog(Greetings(bot))
    for filename in os.listdir("./cmds"):
        if filename.endswith('.py'):
            bot.load_extension(f"cmds.{filename[:-3]}")
    
        
    bot.run(TOKEN)
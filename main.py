"""
Main GoodGames bot entry file.
This is what you run to start the bot.
"""

import disnake
from disnake.ext import commands
from config import DISCORD_TOKEN

# Intents
intents = disnake.Intents.all()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")

    # Load cogs
    for cog in ["cogs.moderation","cogs.rules"]:
        try:
            bot.load_extension(cog)
            print(f"✅ {cog} has been loaded")
        except Exception as e:
            print(f"❌ {cog} has not been loaded.\nReason: {e}")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await cts.send("❌ You do not have permission to use this command.", ephemeral=True)
    elif isinstance(error, commands.MissingRole):
        await ctx.send("❌ You do not have the required role.", ephemeral=True)
    else:
        print(f"Error: {error}")

if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)
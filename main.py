import discord
from discord import File
from discord.ext import commands
from dotenv import load_dotenv
import time
import os.path
import importgames

load_dotenv()
token = os.environ["TOKEN"]

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    await bot.tree.sync()

@bot.command()
async def bghelp(ctx):
    # delete command call
    try:
        await ctx.message.delete()
    except discord.Forbidden:
        await ctx.send("I don't have permission to delete messages.")

    # send help message
    images = ['./media/collection_ref.png', './media/download_ref.png']
    files = [File(path) for path in images]
    try:
        await ctx.author.send('''
        **boardgame-bot help**
               
        - **/addgames**: Add games to the database, this option will only accept csv files, more specifically exported from boardgamegeek.com. Go ahead and add all your owned games to your BGG collection and export them as a csv file. Then upload the file to discord with the /addgames command to add them to the database.
        ''', files=files)
    except discord.Forbidden:
        await ctx.send("I can't send you a private message. Check your DM settings.")

@bot.tree.command(name="addgames", description="Add games to the database")
async def addgames(interaction: discord.Interaction, bgg_csv: discord.Attachment):
    # check first if the attachment is a csv file
    if bgg_csv.filename[-4:] != ".csv":
        await interaction.response.send_message(f'Error: {bgg_csv.filename} is not a csv file')
        return
    else:
        filename = os.path.join('./tmp', interaction.user.name + "_" + time.strftime("%H-%M-%S") + "_" + bgg_csv.filename)
        await bgg_csv.save(filename)
        importgames.add_games_db(interaction.user.name, filename)
        await interaction.response.send_message(f'Added {bgg_csv.url} to the database')

bot.run(token)

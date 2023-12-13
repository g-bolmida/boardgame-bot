import discord 
from discord import File
from discord.ext import commands
from dotenv import load_dotenv
import datetime
import random
import asyncio
import db
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
        - `/addgames`: Add games to the database, this option will only accept csv files, more specifically exported from boardgamegeek.com. Go ahead and add all your owned games to your BGG collection and export them as a csv file. Then upload the file to discord with the `/addgames` command to add them to the database.
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
        await interaction.response.send_message(f'Updated your games to the database')

@bot.tree.command(name="collection", description="Show your collection")
async def collection(interaction: discord.Interaction):
    # create db session
    Session = db.sessionmaker(bind=db.engine)
    session = Session()
    # query the user's collection
    user = session.query(db.User).filter(db.User.name == interaction.user.name).first()
    if user:
        games = user.games
        if games:
            msg = f"{interaction.user.name}'s games:\n"
            for game in games:
                msg += f"- {game.name} [Players: {game.min_players} - {game.max_players}]\n"
            await interaction.response.send_message(msg)
        else:
            await interaction.response.send_message(f"{interaction.user.name} does not own any games.")
    else:
        await interaction.response.send_message(f"User '{interaction.user.name}' not found.")

@bot.tree.command(name="schedule", description="Schedule an event")
async def schedule(interaction: discord.Interaction, event_datetime: str, location: str):
    try:
        event_date_obj = datetime.datetime.strptime(event_datetime, "%Y-%m-%d %H:%M")
        await interaction.response.send_message(f"@everyone RSVP for Boardgames & Beer on {event_date_obj.strftime('%Y-%m-%d at %H:%M')} @ {location}")
        message = await interaction.original_response()
        
        await message.pin()
        await message.add_reaction('✅')
        await message.add_reaction('❌')

        await asyncio.sleep(10)

        # Fetch the updated message to get the reactions
        channel = interaction.channel
        rsvp_message = await channel.fetch_message(message.id)

        yes_reactors = []
        no_reactors = []
        for reaction in rsvp_message.reactions:
            async for user in reaction.users():
                if user != bot.user:
                    if str(reaction.emoji) == '✅':
                        yes_reactors.append(user.name)
                    elif str(reaction.emoji) == '❌':
                        no_reactors.append(user.name)

        Session = db.sessionmaker(bind=db.engine)
        session = Session()

        matching_games = session.query(db.Games).join(db.User.games).filter(db.User.name.in_(yes_reactors), db.Games.min_players <= len(yes_reactors)).all()

        # List of emojis for reactions
        emojis = [
        '😀', '😃', '😄', '😁', '😆', '😅', '🤣', '😂', '🙂', '🙃', 
        '😉', '😊', '😇', '🥰', '😍', '🤩', '😘', '😗', '☺️', '😚', 
        '😙', '😋', '😛', '😜', '🤪', '😝', '🤑', '🤗', '🤭', '🤫', 
        '🤔', '🤐', '🤨', '😐', '😑', '😶', '😏', '😒', '🙄', '😬', 
        '🤥', '😌', '😔', '😪', '🤤', '😴', '😷', '🤒', '🤕', '🤢', 
        '🤮', '🤧', '🥵', '🥶', '🥴', '😵', '🤯', '🤠', '🥳', '😎', 
        '🤓', '🧐', '😕', '😟', '🙁', '😮', '😯', '😲', '😳', '🥺', 
        '😦', '😧', '😨', '😰', '😥', '😢', '😭', '😱', '😖', '😣', 
        '😞', '😓', '😩', '😫', '🥱', '😤', '😡', '😠', '🤬', '😈', 
        '👿', '💀', '☠️', '💩', '🤡', '👹', '👺', '👻', '👽', '👾', 
        '🤖', '😺', '😸', '😹', '😻', '😼', '😽', '🙀', '😿', '😾', 
        '🙈', '🙉', '🙊', '💢', '💥', '💫', '💦', '💨', '🕳️', '💣',
        '💬', '🗨️', '🗯️', '💭', '💤', '👋', '🤚', '🖐️', '✋',
        '🖖', '👌', '🤏', '✌️', '🤞', '🤟', '🤘', '🤙', '👈', '👉',
        '👆', '🖕', '👇', '☝️', '👍', '👎', '✊', '👊', '🤛', '🤜',
        '👏', '🙌', '👐', '🤲', '🤝', '🙏', '✍️', '💅', '🤳', '💪',
        '🦾', '🦵', '🦿', '🦶', '👣', '👂', '🦻', '👃', '🧠', '🦷',
        '🦴', '👀', '👁️', '👅', '👄', '💋', '🩸', '👶', '👧', '🧒',]

        chosen_reactors = []

        # Adding reactions to the message
        for _ in range(len(matching_games)):
            chosen_reactors.append(random.choice(emojis))

        if matching_games:
            games_message = "Vote on the games you would like to play:\n"
            for game in matching_games:
                games_message += f"- {game.name} - <{game.bgg_url}> {chosen_reactors[matching_games.index(game)]}\n"
        else:
            games_message = "No games found suitable for the number of players."

        game_choices = await interaction.followup.send(games_message)

        # Adding reactions to the message
        for x in range(len(matching_games)):
            time.sleep(0.5)
            await game_choices.add_reaction(chosen_reactors[x])

    except ValueError:
        await interaction.response.send_message("Invalid date and time format. Please use YYYY-MM-DD HH:MM.")

bot.run(token)

import asyncio
import dill as pickle
from pymongo import MongoClient
import discord
from discord.ext import commands
from game import Game
from canvas import get_image_from_url, generate_image, generate_bytes
from credentials import discord_bot_token, mongodb_url

client = MongoClient(mongodb_url)

db = client["fightbot"]
game_collection = db["game_data"]
images_collection = db["images"]

PREFIX = '>>'
EMOJI = '▶️'
EMBED_COLOR = 0x307897
MIN_PLAYERS = 4
MAX_PLAYERS = 20

client = commands.Bot(command_prefix=PREFIX)

def make_embed(text):
    return discord.Embed(color=EMBED_COLOR, description=text)

async def check_game_exists(channel):
    if game_collection.count_documents({'_id': channel.id}) > 0:
        embed = make_embed("Game already created in this channel")
        await channel.send(embed=embed)
        return True
    return False

async def check_game_doesnt_exist(channel):
    if game_collection.count_documents({'_id': channel.id}) == 0:
        embed = make_embed(("No game created in this channel,\n"
                            "Use command `>>new` to make a new one"))
        await channel.send(embed=embed)
        return True
    return False

async def check_game_doesnt_exist_quitely(channel):
    if game_collection.count_documents({'_id': channel.id}) == 0:
        return True
    return False

async def check_game_started(channel):
    if game_collection.count_documents({'_id': channel.id, 'game': {'$exists' : True}}) > 0:
        embed = make_embed("Game already started :(")
        await channel.send(embed=embed)
        return True
    return False

async def check_game_not_started(channel):
    if game_collection.count_documents({'_id': channel.id, 'game': {'$exists' : True}}) == 0:
        embed = make_embed("Game not started yet!")
        await channel.send(embed=embed)
        return True
    return False

async def check_player_joined(channel, player):
    if game_collection.count_documents({'_id': channel.id, 'player_ids': player.id}) > 0:
        embed = make_embed("You already joined!")
        await channel.send(embed=embed)
        return True
    return False

async def check_max_players_joined(channel):
    if game_collection.count_documents({'_id': channel.id,
        'player_ids.' + str(MAX_PLAYERS - 1): {"$exists": True}}) > 0:
        embed = make_embed("No more players can join :(")
        await channel.send(embed=embed)
        return True
    return False

async def check_not_game_creator(channel, player):
    if game_collection.count_documents({'_id': channel.id, 'game_creator': player.id}) == 0:
        embed = make_embed("Only game creator do this")
        await channel.send(embed=embed)
        return True
    return False

async def check_not_game_creator_quitely(channel, player):
    if game_collection.count_documents({'_id': channel.id, 'game_creator': player.id}) == 0:
        return True
    return False

async def check_less_than_min_players_joined(channel):
    if game_collection.count_documents({'_id': channel.id,
        'player_ids.' + str(MIN_PLAYERS - 1): {"$exists": True}}) == 0:
        embed = make_embed("Too few players :(")
        await channel.send(embed=embed)
        return True
    return False

def check_not_reaction_message(channel, message):
    if game_collection.count_documents({'_id': channel.id, 'reaction_message': message.id}) == 0:
        return True
    return False

def add_player(channel, name, _id, image):
    game_collection.update_one(
        {'_id': channel.id},
        {
            '$push': 
            {
                'player_names': name, 
                'player_ids': _id, 
            }
        }
    )
    images_collection.insert_one({'_id': _id, 'image': pickle.dumps(image)})

def add_game(channel):
    document = game_collection.find_one(
        {'_id': channel.id}, 
        {'_id': 0, 'player_names': 1, 'player_ids': 1}
    )
    game = Game(document['player_names'], document['player_ids'])
    dumped_game = pickle.dumps(game)
    game_collection.update_one(
        {'_id': channel.id},
        {'$set': {'game': dumped_game}}
    )

async def tick_game(channel):
    document = game_collection.find_one(
        {'_id': channel.id}, 
        {'_id': 0, 'game': 1}
    )
    dumped_game = document['game']
    game = pickle.loads(dumped_game)
    text, players, is_finished = game.tick()

    game_collection.update_one(
        {'_id': channel.id}, 
        {'$set': {'game': pickle.dumps(game)}}
    )

    images = []
    for player in players:
        image_document = images_collection.find_one({'_id': player.get_index()})
        dumped_image = image_document['image']
        image = pickle.loads(dumped_image)
        images.append(image)

    embed = make_embed(text)
    file = discord.File(generate_bytes(generate_image(images, players)), filename="image.png")
    msg = await channel.send(file=file, embed=embed)
    if is_finished:
        await exit_game(channel)
        return
    await msg.add_reaction(EMOJI)
    game_collection.update_one({'_id': channel.id}, {'$set': {'reaction_message': msg.id}})

async def exit_game(channel):
    embed = make_embed("Game ended")
    await channel.send(embed=embed)

    ids = game_collection.find_one({'_id': channel.id})['player_ids']

    for _id in ids:
        images_collection.delete_one({'_id': _id})
    game_collection.delete_one({'_id': channel.id})

@client.event
async def on_ready():
    client.loop.create_task(update_status())
    print('logged in as {0.user}'.format(client))

@client.command()
async def new(ctx):
    if await check_game_exists(ctx.channel):
        return
    embed = make_embed((
        f"A new game created by {ctx.author.display_name}!\n"
        "Use command `>>join` to let yourself in,\n"
        "Game creator can use `>>add <player name> {player image url}` "
        "to add custom players (you can also embed an image instead of "
        "using a url),\n"
        "Use `>>start` to begin the game,\n"
        "Use `>>quit` to terminate current game\n"
        "A minimum of 4 and a maximum of 20 players can join"))
    game_collection.insert_one({
        "_id": ctx.channel.id,
        "player_names": [],
        "player_ids": [],
        "game_creator": ctx.author.id
    })
    await ctx.send(embed=embed)

@client.command()
async def join(ctx):
    if  await check_game_doesnt_exist(ctx.channel) or \
        await check_game_started(ctx.channel) or \
        await check_player_joined(ctx.channel, ctx.author) or \
        await check_max_players_joined(ctx.channel):
        return
    
    image = get_image_from_url(ctx.author.avatar_url)
    if isinstance(image, str):
        embed = make_embed(image)
        await ctx.channel.send(embed=embed)
        return
    
    add_player(ctx.channel, ctx.author.display_name, ctx.author.id, image)

    embed = make_embed('**' + ctx.author.display_name + ' has joined' + '**')
    file = discord.File(generate_bytes(generate_image(image)), filename="image.png")
    await ctx.channel.send(file=file, embed=embed)

@client.command()
async def add(ctx, name, image_url=None):
    if  await check_game_doesnt_exist(ctx.channel) or \
        await check_game_started(ctx.channel) or \
        await check_max_players_joined(ctx.channel):
        return
    
    if image_url is None and len(ctx.message.attachments) == 0:
        embed = make_embed("Invalid command")
        await ctx.channel.send(embed=embed)
        return

    if image_url is None:
        image = get_image_from_url(ctx.message.attachments[0].url)
    else:
        image = get_image_from_url(image_url)
    
    if isinstance(image, str):
        embed = make_embed(image)
        await ctx.channel.send(embed=embed)
        return

    add_player(ctx.channel, name, int('1' + str(ctx.message.id)), image)

    embed = make_embed('**' + name + ' has joined' + '**')
    file = discord.File(generate_bytes(generate_image(image)), filename="image.png")
    await ctx.channel.send(file=file, embed=embed)

@client.command()
async def start(ctx):
    if  await check_game_doesnt_exist(ctx.channel) or \
        await check_game_started(ctx.channel) or \
        await check_not_game_creator(ctx.channel, ctx.author) or \
        await check_less_than_min_players_joined(ctx.channel):
        return
    
    add_game(ctx.channel)

    embed = make_embed(f"Game started!!\nGame creator can react with {EMOJI} or use `>>next` to proceed")
    await ctx.channel.send(embed=embed)

    await tick_game(ctx.channel)

@client.command(name = 'next')
async def _next(ctx):
    if  await check_game_doesnt_exist(ctx.channel) or \
        await check_game_not_started(ctx.channel) or \
        await check_not_game_creator(ctx.channel, ctx.author):
        return
    
    await tick_game(ctx.channel)

@client.command(name='quit')
async def _quit(ctx):
    if  await check_game_doesnt_exist(ctx.channel) or \
        await check_not_game_creator(ctx.channel, ctx.author):
        return
    
    await exit_game(ctx.channel)

@client.event
async def on_reaction_add(reaction, user):
    if user == client.user or user.bot:
        return

    if  reaction.emoji != EMOJI or \
        await check_game_doesnt_exist_reaction(reaction.message.channel) or \
        await check_not_game_creator_reaction(reaction.message.channel, user) or \
        check_not_reaction_message(reaction.message.channel, reaction.message):
        return

    await tick_game(reaction.message.channel)

async def update_status():
    while True:
        with open('res/botstatus.txt', 'r') as status_file:
            status = status_file.read()
        await client.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.playing,
                name=status
            )
        )
        await asyncio.sleep(60)

client.run(discord_bot_token)

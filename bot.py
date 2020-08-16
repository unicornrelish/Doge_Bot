#Doge_Bot - Ver 0.1.0
import discord
from discord.ext import commands,tasks
import time
import asyncio
from itertools import cycle
import os
from var import steam_group_url, mcserver_ip, bot_cmd_channel, ver, owner, mod_channel_id, guild, TOKEN, b_words, bot, mod_role


ready_act = discord.Game(f'on version {ver}')
processing_act = discord.Game('with the code.')



messages = joined = 0

cmd_prefix='!'

GUILD = guild

description = 'The Dogenet Incorporated Master Bot'
bot = commands.Bot(command_prefix=cmd_prefix, description=description)


#Sets the load message when not idle.
async def load():
    await bot.change_presence(activity=processing_act, status=discord.Status.online)

#Sets the idle message when not under load.
async def idle():
    await bot.change_presence(status=discord.Status.idle, activity=ready_act)

#Updates the stats file and log file.
async def update_stats():
    await bot.wait_until_ready()
    global messages, joined

    while not bot.is_closed():
        try:
            with open('stats.txt', 'a') as f:
                f.write(f'Time: {int(time.time())}, Messages: {messages}, Members Joined: {joined}\n')
            
            messages = 0
            joined = 0
            await asyncio.sleep(1200)
        except Exception as e:
            print(e)
            await asyncio.sleep(1200)

async def update_logs():
    await bot.wait_until_ready()


cogs = ['cogs.utilities']
#Initiates the bot.
@bot.event
async def on_ready():
    await load()
    guild = discord.utils.find(lambda g: g.name == GUILD, bot.guilds)
    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
        )
    bot.remove_command('help')
    # Removes the help command
    # Make sure to do this before loading the cogs
    for cog in cogs:
        bot.load_extension(cog)
    await idle()

#Sends a new user a message prompting them to get their role.
@bot.event
async def on_member_join(member):
    await load()
    global joined
    joined += 1
    await member.create_dm()
    await member.dm_channel.send(
        'Read the rules in the rules channel to learn your rights.'
        )
    await print(f'{member} joined the server.')
    await idle()

#Gives user role after reacting to the message in rules.
@bot.event
async def on_raw_reaction_add(payload):
    await load()
    message_id = payload.message_id
    #Verifies the message ID
    if message_id == 740026078554357770:
        guild = discord.utils.find(lambda g : g.name == GUILD, bot.guilds)

        #Looks for the cool_doge emoji.
        if payload.emoji.name == 'cool_doge':
            role = discord.utils.get(guild.roles, name='Nutlings')
        else:
            role = discord.utils.get(guild.roles, name=payload.emoji.name)
        
        #Prints the role and name of the member after giving them their role.
        if role is not None:
            member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
            if member is not None:
                await member.add_roles(role)
                print(
                    f'{role.name} role given to {member.name}.')
                #await client.change_presence(status=discord.Status.dnd, activity=discord.Streaming(name=
                #'Family Guy Funny Moments', url='https://www.youtube.com/watch?v=Zxl28UgHpn0'))
            else:
                print('Member not found.')
        else:
            print('Role not found.')
            print(payload.emoji.name)
    await idle()


#Removes the role if the user removes their emote from the rules message.
@bot.event
async def on_raw_reaction_remove(payload):
    await load()
    message_id = payload.message_id

    #Verifies the message ID
    if message_id == 740026078554357770:
        guild = discord.utils.find(lambda g : g.name == GUILD, bot.guilds)
        
        #Looks for the cool_doge emoji.
        if payload.emoji.name == 'cool_doge':
            role = discord.utils.get(guild.roles, name='Nutlings')
        else:
            role = discord.utils.get(guild.roles, name=payload.emoji.name)

        #Prints the role and name of the member after removing their role.
        if role is not None:
            member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
            if member is not None:
                await member.remove_roles(role)
                await bot.change_presence(activity=discord.Game('on the floor.'))
                print(
                    f'{role.name} role taken from {member.name}.')
                #await client.change_presence(status=discord.Status.dnd, activity=discord.Streaming(name=
                #'Family Guy Funny Moments', url='https://www.youtube.com/watch?v=Zxl28UgHpn0'))
            else:
                print('Member not found.')
        else:
            print('Role not found.')
            print(payload.emoji.name)
    await idle()

@bot.event # This event runs whenever a user updates: status, game playing, avatar, nickname or role
async def on_member_update(before, after): 
    n = after.nick 
    if n: # Check if they updated their username
        if n.lower().count(owner) > 0: # If username contains the owner's username
            last = before.nick
            if last: # If they had a username before change it back to that
                await after.edit(nick=last)
            else: # Otherwise set it to "LIAR"
                await after.edit(nick="LIAR")

#Filters certain slurs.
@bot.event 
async def on_message(message):
    await load()
    global messages
    channel = message.channel
    author = message.author
    mod_channel = bot.get_channel(mod_channel_id)

    #This is the start of defining which commands do what.
    if message.content.startswith(cmd_prefix):
            
#~~~~~~~~~~~~~~~~~~~~~~DISCONNECT COMMAND~~~~~~~~~~~~~~~~~~~~~~
        #Disconnects the bot from the websocket.
        if message.content.startswith('!disconnect'):
            print(f'{author} sent "!disconnect" command in {channel}.')
            if str(message.channel) == bot_cmd_channel:
                if str(author) == owner:
                    await message.channel.send(f"This command isn't ready yet...")
            else:
                await message.delete()
                print(f"Deleted! Command wasn't in correct channel({bot_cmd_channel}")
#~~~~~~~~~~~~~~~~~~~~~~~~STEAM COMMAND~~~~~~~~~~~~~~~~~~~~~~~~~
        if message.content.startswith('!steam'):
            embed = discord.Embed(title= "Steam Group URL", description= steam_group_url)
            await message.channel.send(content=None, embed=embed)
            print(f'{author} sent "!steam" command in {channel}.')
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #Increases messages count.
    messages += 1
#~~~~~~~~~~~~~~~~~~~~~~~~~SLUR FILTER~~~~~~~~~~~~~~~~~~~~~~~~~~
    if channel != mod_channel:
        for badword in b_words:
            if badword in message.content.lower():
                await message.delete()
                await message.channel.send(f"{message.author.mention}!\nUh oh!\nYou shouldn't have said that!")
                if str(author) != bot:
                    await mod_channel.send(f"<@&{mod_role}>! {message.author} said: '{message.content}'")
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    await bot.process_commands(message)
    await idle()

        
bot.loop.create_task(update_stats())
bot.run(TOKEN)

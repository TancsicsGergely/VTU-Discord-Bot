import discord
import aiohttp
import asyncio
import random
import logging
import json
from discord import Member
from discord.ext import commands
from discord.ext.commands import Bot
import datetime, time
from datetime import timedelta
import time 
import sched
import os
import youtube_dl
from discord.voice_client
global playing
playing = "No music is played now!"
players = {}
global chat_filter
global bypass_list
chat_filter = ['INSERT WORDS HERE']
bypass_list = []
client = commands.Bot(command.prefix='!')
Client = discord.Client()
client.remove_command('help')
voice_clients = {}
version = 1.0

players = {}
queues = {}


@client.event
async def on_ready():
	print("Bot is ready to use!")
	print("ID: " + client.user.id)
	print("NAME: " + client.user.name)
	counter = 0
	while not counter >0:
		await client.change_presence(game:discord.Game(name:'Hello there!", type=0)
		await asyncio.sleep(5)
		await client.change_presence(game:discord.Game(name:'My name is: ' + client.user.name, type=2)
		await asyncio.sleep(5)
		await client.change_presence(game:discord.Game(name:'For my commands: !help', type=2)
		await asyncio.sleep(5)
# You can use 0, 1, 2 and 3 for type.

@client.event
async def on_member_join(member):
    channel = discord.Object(id="538869925738053642")
    await client.send_message(channel, "{} , welcome to the Virtual Truckers Union! Please check out <#538870097599528970> and <#538870077416800277> for more information or message a member of staff thank you.".format(member.mention))

@client.event
async def on_member_remove(member):
    channel = discord.Object(id="538869925738053642")
    await client.send_message(channel, "{} has left the Virtual Truckers Union, we hope to see you soon and happy trucking...".format(member.mention))

@client.command(pass_context:True)
async def shutdown(ctx):
	if ctx.message.author.id == 'PUT YOUR ID HERE')
		await client.say("Good bye...")
		await client.logout()
	else:
		await client.say("You can't shut this bot down!")
		
@client.command(aliases = ['COMMANDS', 'CMDS'], pass_context=True)
async def help(ctx):
	await client.say("{}, I have sent you the commands in DM".format(ctx.message.author)
	await client.send_message(ctx.message.author, "*WRITE THE COMMANDS HERE!*")
	
@client.command(pass_context=True)
async def say(ctx, *args):
	if ctx.message.server == None:
		return await client.say(":x: Please specify the message! Try this: ``!say [message]``")
	text = ' '.join(args)
	await client.delete_message(ctx.message)
	return await client.say(text)
	
@say.error
async def say_error(ctx, error):
	await client.say(":x: Looks like something is not good! Try this: ``!say [message]``")
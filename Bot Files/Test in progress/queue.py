import discord
import aiohttp
import asyncio
import random
import logging
import json
import requests
from discord import Member
from discord.ext import commands
from discord.ext.commands import Bot
import datetime, time
from datetime import timedelta
import time
import sched
import os
import youtube_dl
from discord.voice_client import VoiceClient
from discord_webhook import DiscordWebhook, DiscordEmbed
from emojis import emojis
from pyson import pyson
global playing
playing = "No music playing right now :("
players = {}
client = commands.Bot(command_prefix='!VTU ')
Client = discord.Client()
client.remove_command('help')
voice_clients = {}
version = 1.0

players = {}
queues = {}



songs = asyncio.Queue()
play_next_song = asyncio.Event()


async def audio_player_task():
    while True:
        play_next_song.clear()
        current = await songs.get()
        current.start()
        await play_next_song.wait()


def toggle_next():
    client.loop.call_soon_threadsafe(play_next_song.set)


@client.command(pass_context=True)
async def testplay(ctx, * ,url, ytdl_options=None, **kwarg):
        if not ctx.message.author.bot:
            server = ctx.message.server
            voice_client = client.voice_client_in(server)
            if voice_client == None:
                await client.say("Please wait. :musical_note:")
                try:
                    channel = ctx.message.author.voice.voice_channel
                    await client.join_voice_channel(channel)
                except:
                    return False
                try:
                    server = ctx.message.server
                    voice_client = client.voice_client_in(server)
                    ydl_opts = {
                        'format': 'bestaudio/best',
                        'postprocessors': [{
                            'key': 'FFmpegExtractAudio',
                            'preferredcodec': 'mp4',
                            'preferredquality': '192',
                        }],
                    }
                    player = await voice_client.create_ytdl_player("ytsearch: {}".format(url), before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5", after=toggle_next)
                    player.start()
                    await songs.put(player)
                    global playing
                    await client.say("Starting the music...\nTitle: **{}**".format(player.title))
                    global players
                    players[server.id] = player 
                    player.volume = 0.2
                    global playing 
                    playing = "Now playing: **{}**".format(player.title)
                    global last_played
                    last_played = player.url
#                    embed = discord.Embed(title="Music Player", description="Informations: ", color=0x00ff00)
#                    embed.add_field(name="Song title:",value=player.title, inline=True)
#                    embed.add_field(name="Date of uploading:",value=player.upload_date, inline=True)
#                    embed.add_field(name="Uploader:",value=player.uploader, inline=True)
#                    embed.add_field(name="Requested by:",value=ctx.message.author,inline=True)
#                    embed.set_author(name=ctx.message.author.name, icon_url=ctx.message.author.icon_url)
#                    await client.say(embed=embed)
#                    await client.say(embed=embed)
                except:
                    await client.say("Oops! Something went wrong. Please try ``!VTU leave`` and try again. :x:")
                while not player.is_done():
                    await asyncio.sleep(1)
                    player = await voice.create_ytdl_player(url, after=toggle_next)
                    await songs.put(player) 
                try:
                    server = ctx.message.server
                    voice_client = client.voice_client_in(server)
                    await voice_client.disconnect()
                    await client.say("The song is over. I left the voice channel. :white_check_mark: ")
                except:
                    return False
            else:
                await client.say("Something is not good! Use ``!VTU leave``!")
        else:
            return False

        

client.loop.create_task(audio_player_task())
client.run("TOKEN")

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


def toggle_next(self):
    self.client.loop.call_soon_threadsafe(play_next_song.set)


@client.command(aliases=['tp'], pass_context=True)
async def testp(ctx, * ,url, ytdl_options=None, **kwargs):
    '''Usage: !VTU play [music]'''
    try:
        if not ctx.message.author.bot:
            if not client.is_voice_connected(ctx.message.server):
                voice = await client.join_voice_channel(ctx.message.author.voice_channel)
            else:
                voice = client.voice_client_in(ctx.message.server)
            await client.say("Loading music, please wait... :musical_note:")
            player = await voice.create_ytdl_player("ytsearch: {}".format(url), before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5", after=toggle_next)
            await songs.put(player)
            await client.say("Starting the music! {}\nTitle: **{}**".format(emojis['done'], player.title))
            global playing
            global players
            server = ctx.message.server
            players[server.id] = player 
            player.volume = 0.2
            global playing
            playing = "Now playing: **{}**".format(player.title)
            global last_played
            last_played = player.url
        else:
            return False
    except Exception as e:
        print(e)

@testp.error
async def testp_error(self, ctx, error):
    print(error)
    await self.client.say("Something went wrong! Please contact <@414391316059783172>!\n***Errors:***\n**{}**\n**{}**\n**{}**".format(EnvironmentError, EOFError, error))

@client.command(aliases=['np', 'playing'], pass_context=True)
async def now(ctx):
    if not ctx.message.author.bot:
        global playing
#        await self.client.say(playing)
        embed = discord.Embed(title=None, description="{}".format(playing), color=0x00f12)
        embed.set_footer(text="VTU Discord Bot | v{}".format(version))
        embed.set_author(name="Current music", icon_url="https://cdn.discordapp.com/attachments/563361610530422784/576845858339815435/vtulogo.webp")
        await client.say(embed=embed)
        del playing
    else:
        return False


client.loop.create_task(audio_player_task())
client.run("TOKEN")

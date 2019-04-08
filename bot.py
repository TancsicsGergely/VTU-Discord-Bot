import aiohttp
import discord
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
from discord.voice_client import VoiceClient
global playing
playing = "No music playing right now :("
players = {}
global chat_filter
global bypass_list
chat_filter = ["FUCK", "DICK", "SHIT", "FUCKING", "BITCH"]
bypass_list = []
client = commands.Bot(command_prefix='!test ')
Client = discord.Client()
client.remove_command('help')
voice_clients = {}
version = 1.0

players = {}
queues = {}

@client.event
async def on_ready():
    print ("The bot is ready to use.")
    print ("Name: " + client.user.name)
    print ("ID: " + client.user.id)
    counter = 0
    while not counter >0:
        await client.change_presence(game=discord.Game(name='over the VTU...', type=3))
        await asyncio.sleep(5)
        await client.change_presence(game=discord.Game(name='VTU Discord Bot | v1.0', type=3))
        await asyncio.sleep(5)
        await client.change_presence(game=discord.Game(name='Virtual Truckers Union', url="https://www.twitch.tv/", type=1))
        await asyncio.sleep(5)



#---------------------------------------------------------------------------------------------------------------------------------#

@client.event
async def on_message(message) :
    global chat_filter
    global bypass_list
    await client.process_commands(message)
    contents = message.content.split(" ")
    for word in contents:
        if word.upper() in chat_filter:
            if not message.author.id in bypass_list:
                try:
                    await client.delete_message(message)
                    await client.send_message(message.channel, "Hey! Please watch your language! :angry:")
                except discord.errors.NotFound:
                    return


@client.event
async def on_member_join(member):
    channel = discord.Object(id="564862628946640916")
    await client.send_message(channel, "{} , welcome to the Virtual Truckers Union! Please check out <#538870097599528970> and <#538870077416800277> for more information or message a member of staff thank you.".format(member.mention))

@client.event
async def on_member_remove(member):
    channel = discord.Object(id="564862628946640916")
    await client.send_message(channel, "{} has left the Virtual Truckers Union, we hope to see you soon and happy trucking...".format(member.mention))
#--------------------------------------------------------------------------------------------------------------------------------#



#-------------------------------------------------------Dev tools----------------------------------------------------------------#

@client.command(pass_context=True)
async def file(ctx):
    await client.send_typing(ctx.message.channel)
    await asyncio.sleep(1)
    await client.send_file(ctx.message.channel.author, "VTUBot.py")

@client.command(pass_context=True)
async def servers(ctx):
    msg = await client.say("Fetching info...")
    await asyncio.sleep(0.5)
    await client.edit_message(msg, "I'm in **{}** server(s)!".format(str(len(client.servers))))


    
@client.command(pass_context=True)
async def shutdown(ctx):
    if ctx.message.author.id == '414391316059783172' or ctx.message.author.id == '137977201344643072':
        await client.say("I'm shutting down!")
        await client.logout()
    else:
        await client.say("You can't turn off the bot!")
    







#----------------------------------------------------------Moderating cmds-------------------------------------------------------#

@client.command(pass_context=True)
async def purge(ctx, amount=301):
    '''Usage: !VTU purge [amount]'''
    if ctx.message.author.server_permissions.administrator or ctx.message.author.id == '416226732966936577':
        try:
            channel = ctx.message.channel
            messages = []
            async for message in client.logs_from(channel, limit=int(amount) + 1):
                messages.append(message)
            await client.delete_messages(messages)
            await client.say(":white_check_mark: Messages deleted. :thumbsup:")
        except:
            print (Exception)
            await client.say("The number must be between 1 and 300 and the message be maximum 14 days old.:x:")
    else:
        await client.say("You need Admin perms to use this. :x:")



@client.command(pass_context=True, no_pm=True)
async def kick(ctx, user: discord.Member, * ,reason : str = None):
    '''Usage: !VTU kick [member] [reason]'''
    if not ctx.message.author.bot:
        if ctx.message.author.server_permissions.administrator or ctx.message.author.role.id == '&539595654331236353' or ctx.message:
            if reason == "None":
                reason = "(No reason logged!)"
            await client.send_message(user, "You're kicked from **{}** server for this: **".format(ctx.message.server.name) + reason + "**")
            await client.say("Bye, {}. You got kicked :D".format(user.mention))
            await client.kick(user)  
        else:
            await client.say("You need Admin prems to use this! :x:")
    else:
        return False


@client.command(pass_context = True)
async def ban(ctx, member: discord.Member, days: int, *, reason : str = None):
    if ctx.message.author.server_permissions.administrator or ctx.message.author.role.id == '&539595654331236353' or ctx.message.author.server_permissions.ban:
        if reason == "None":
            reason = "(No reason logged!)"
        await client.send_message(member, "You got banned from this server {} for {} days for this reason: **{}**".format(ctx.message.server.name, days ,reason)) 
        await client.say(":white_check_mark: I banned this member! :thumbsup:")
        await client.ban(member, days)
    else:
        await client.say("You need Admin perms to use this :x:")


@client.command(pass_context = True)
async def mute(ctx, member: discord.Member):
    '''Usage: !VTU mute [mention] Role named "Muted" needed! '''
    if ctx.message.author.server_permissions.administrator or ctx.message.author.role.id == '&539595654331236353' or ctx.message.author.server_permissions.manageRoles or ctx.message.author.id == '416226732966936577' or ctx.message.author.id == '497797334684401664':
        role = discord.utils.get(member.server.roles, name='Muted')
        await client.add_roles(member, role)
        embed=discord.Embed(title="User muted!", description="**{0}** muted by **{1}** . :white_check_mark: ".format(member.mention, ctx.message.author.mention), color=0xff00f6)
        await client.say(embed=embed)
    else:
        embed=discord.Embed(title="Permission denied!", description="You don't have permission to use this command. :x:", color=0xff00f6)
        await client.say(embed=embed)



@client.command(pass_context = True)
async def unmute(ctx, member: discord.Member):
    '''Usage: !VTU mute [mention] Role named "Muted" needed! '''
    if ctx.message.author.server_permissions.administrator or ctx.message.author.role.id == '&539595654331236353' or ctx.message.author.server_permissions.manageRoles or ctx.message.author.id == '416226732966936577' or ctx.message.author.id == '497797334684401664':
        role = discord.utils.get(member.server.roles, name='Muted')
        await client.remove_roles(member, role)
        embed=discord.Embed(title="User unmuted!", description="**{0}** unmuted by **{1}** . :white_check_mark: ".format(member.mention, ctx.message.author.mention), color=0xff00f6)
        await client.say(embed=embed)
    else:
        embed=discord.Embed(title="Permission denied!", description="You don't have permission to use this command. :x:", color=0xff00f6)
        await client.say(embed=embed)



@client.command(pass_context=True)
async def warn(ctx, member: discord.Member, *, reason : str = None):
    if not ctx.message.author.bot or ctx.message.author.role.id == '&539595654331236353' :
        await client.delete_message(ctx.message)
        await client.send_message(member, "You received a warn from **{}** from this server: **{}** . Reason: **{}**".format(ctx.message.author , ctx.message.server.name , reason))
        await client.say(":white_check_mark: I sent the warn!! :thumbsup:")
    else:
        return False

#-------------------------------------------------------------------------------------------------------------------------------#






#----------------------------------------------------------------Others----------------------------------------------------------#

@client.command(pass_context=True)
async def poll(ctx, *, message2):
    yes = 0
    no = 0
    await client.delete_message(ctx.message)
    poll = await client.say("**{}**".format(message2))
    await client.add_reaction(poll, '✅')
    await client.add_reaction(poll, '❌')
    reactions = await client.wait_for_reaction(['✅'], message=poll)
    yes = yes + 1
    reactions2 = await client.wait_for_reaction(['❌'], message=poll)
    no = no + 1
    await asyncio.sleep(5)
    await client.say("Vote closed! Results: **{}** ``yes``, **{}** ``no``".format(yes, no))

@poll.error
async def poll_error(ctx, error):
    await client.say(":x: Looks like something is not good! Try this: ``!VTU poll [message]``")



@client.command(pass_context=True)
async def say(ctx, *args):
    if ctx.message.server == None:
        return await client.say(":x: Please specify the message! Try this: ``!VTU say [message]``")
    text = ' '.join(args)
    await client.delete_message(ctx.message)
    return await client.say(text)

@say.error
async def say_error(ctx, error):
    await client.say(":x: Looks like something is not good! Try this: ``!VTU say [message]``")



@client.command(pass_context=True)
async def help(ctx):
    await client.send_message(ctx.message.author, "Hello {}! These are my commands:\n\n:information_source: __**General commands**__ :information_source:\n\n*!VTU info [mention] -* **Shows informations about the mentioned user.**\n*!VTU serverinfo -* **Shows informations about the server where you used this command.**\n*!VTU ping -* **Shows you client's ping in ``ms``.**\n\n:tools: __**Moderation**__ :tools:\n\n*!VTU warn [mention] -* **Warns the mentioned user. (Requires HOO rank)**\n*!VTU mute [mention] -* **Mutes the mentioned user. (Requires administrator/manage roles permission)**\n*!VTU unmute [mention] -* **Unmutes the mentioned user. (Requires administrator/manage roles permission)**\n*!VTU kick [mention] -* **Kicks the mentioned user. (Requires administrator/kick members permission)**\n*!VTU ban [mention] -* **Bans the mentioned user. (Requires administrator/ban members permission)**\n\n:musical_note: Musical commands :musical_note:\n\n*!VTU play [link/name of the music] -* **Plays the requested song.**\n*!VTU leave -* **Leaves the voicechannel.**\n*!VTU pause -* **Pauses the played music. (The bot has to play a music to use this command)**\n*!VTU resume -* **Resumes the paused music.**\n*!VTU stop -* **After using this command you won't be able to resume the music, you'll have to use ``!VTU play`` again.**\n\n:mailbox_with_mail: Good to know :mailbox_with_mail:\n\n*Prefix:*\n**The permanent prefix is ``!VTU ``.**\n*VTU's website:*\nhttps://virtualtruckersunion.net/".format(ctx.message.author.mention))
    await client.say("I've sent you my commands in DM!")

@help.error
async def help_error(ctx, error):
    embed = discord.Embed(title=":warning: Fatal error! :warning:", description=None, color=0xffd11a)
    embed.add_field(name="I can't send you the list of the commands!", value="**Please check that you can receive messages from anyone or that I'm not blocked for you!**", inline=True)
    embed.add_field(name="Error at:", value="**{}**".format(error), inline=True)
    embed.add_field(name="Help us improve user experience!", value="**Please report this problem to <@414391316059783172> to help us solve this awkvard problem.**")
    embed.set_author(name="Unkown error", icon_url=client.user.avatar_url)
    embed.set_footer(text="VTU Discord Bot | v{}".format(version))
    await client.say(embed=embed)



#------------------------------------------------------------------------Public Cmds---------------------------------------------#


@client.command(aliases=['user-info', 'ui'], pass_context=True, invoke_without_command=True)
async def info(ctx, user: discord.Member):
    '''Usage: !VTU info [mention]'''
    if not ctx.message.author.bot:
        try:
            embed = discord.Embed(title="Information from this user: {}".format(user.name), description="Details:", color=0x00ff00)
            embed.add_field(name="Name:", value=user.name, inline=True)
            embed.add_field(name='Nickname:', value=user.nick, inline=True)
            embed.add_field(name="ID:", value=user.id, inline=True)
            embed.add_field(name="Status:", value=user.status, inline=True)
            embed.add_field(name='Game:', value=user.game, inline=True)
            embed.add_field(name="Highest role:", value=user.top_role)
#            embed.add_field(name="Joined at:", value=user.joined_at)
            embed.add_field(name='Joined at:', value=user.joined_at.__format__('%A, %Y. %m. %d. @ %H:%M:%S'))
            embed.set_author(name="User informations", icon_url=user.avatar_url)
            embed.set_thumbnail(url=user.avatar_url)
            embed.set_footer(text="VTU Discord Bot | v{}".format(version))
            await client.say(embed=embed)
        except:
            return False
    else:
        return False



@client.command(pass_context=True)
async def ping(ctx):
    '''A ping command'''
    if not ctx.message.author.bot:
        channel = ctx.message.channel
        t1 = time.perf_counter()
        await client.send_typing(channel)
        t2 = time.perf_counter()
        embed=discord.Embed(title="Pong!", description='This message took around {}ms.'.format(round((t2-t1)*1000)), color=0xffff00)
        await client.say(embed=embed)
    else:
        return False


@client.command(pass_context=True)
async def serverinfo(ctx):
    '''A useful command.'''
    if not ctx.message.author.bot:
        online = 0
        for i in ctx.message.server.members:
            if str(i.status) == 'online' or str(i.status) == 'idle' or str(i.status) == 'dnd':
                online += 1
        role_count = len(ctx.message.server.roles)
        emoji_count = len(ctx.message.server.emojis)
        embed = discord.Embed(title="Information from this server: {}".format(ctx.message.server.name), description="Here it is:", color=0x00ff00)
        embed.add_field(name="Name: ", value=ctx.message.server.name, inline=True)
        embed.add_field(name="ID: ", value=ctx.message.server.id, inline=True)
        embed.add_field(name="Number of roles: ", value=len(ctx.message.server.roles), inline=True)
        embed.add_field(name="Members: ", value=len(ctx.message.server.members))
        embed.add_field(name='Currently online', value=online)
        embed.add_field(name="Server created at: ", value=ctx.message.server.created_at.__format__('%A, %Y. %m. %d.'), inline=True)
#        embed.add_field(name="Channel created at: ",value=ctx.message.channel.created_at.__format__('%A, %Y. %m. %d. @ %H:%M:%S'), inline=True)
#        embed.add_field(name="Current channel: ",value=ctx.message.channel, inline=True)
        embed.add_field(name="Server's owner's name: ",value=ctx.message.server.owner.mention, inline=True)
        embed.add_field(name="Server's owner's status: ",value=ctx.message.server.owner.status, inline=True)
        embed.add_field(name="Server region: ",value=ctx.message.server.region, inline=True)
        embed.add_field(name='Moderation level', value=str(ctx.message.server.verification_level))
        embed.add_field(name='Number of emotes', value=str(emoji_count))
        embed.add_field(name='Highest role', value=ctx.message.server.role_hierarchy[0])
        embed.set_thumbnail(url=ctx.message.server.icon_url)
        embed.set_author(name=ctx.message.server.name, icon_url=ctx.message.server.icon_url)
        await client.say(embed=embed)
    else:
        return False



#--------------------------------------------------------------------Music cmds--------------------------------------------------#


@client.command(aliases=['p'], pass_context=True)
async def play(ctx, * ,url, ytdl_options=None, **kwarg):
    '''Usage: !VTU play [music]'''
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
                player = await voice_client.create_ytdl_player("ytsearch: {}".format(url), before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5")
                player.start()
                global players
                players[server.id] = player 
                player.volume = 0.2
                global playing 
                playing = "Now playing: **{}**".format(player.title)
                global last_played
                last_played = player.url
                embed = discord.Embed(title="Music Player", description="Informations: ", color=0x00ff00)
                embed.add_field(name="Song title",value=player.title, inline=True)
                embed.add_field(name="Upload date",value=player.upload_date, inline=True)
                embed.add_field(name="Uploader",value=player.uploader, inline=True)
                embed.add_field(name="Requested",value=ctx.message.author,inline=True)
                embed.set_author(name=ctx.message.author.name, icon_url=ctx.message.author.icon_url)
                await client.say(embed=embed)
            except:
                print(Exception)
                await client.say("Oops! Something went wrong. Please try ``!VTU leave`` and try again. :x:")
            while not player.is_done():
                await asyncio.sleep(1) 
            try:
                server = ctx.message.server
                voice_client = client.voice_client_in(server)
                await voice_client.disconnect()
                await client.say("The song is over. I left the voice chanbnel. :white_check_mark: ")
            except:
                return False
        else:
             await client.say("It looks like I currently play something! Please try ``!VTU leave`` and try again. :x:")
    else:
        return False


@client.command(pass_context=True)
async def pause(ctx):
    if not ctx.message.author.bot:
        try:
            id = ctx.message.server.id
            players[id].pause()
            await client.say("Paused. :thumbsup:")
        except:
            await client.say("The song is already paused. :x:")
    else:
        return False

@client.command(pass_context=True)
async def resume(ctx):
    if not ctx.message.author.bot:
        try:
            id = ctx.message.server.id
            players[id].resume()
            await client.say("Resumed. :thumbsup:")
        except:
            await client.say("The song is already playing or stopped. :x:")
    else:
        return False

@client.command(pass_context=True)
async def stop(ctx):
    if not ctx.message.author.bot:
        try:
            id = ctx.message.server.id
            players[id].stop()
            server = ctx.message.server
            voice_client = client.voice_client_in(server)
            await voice_client.disconnect()
            await client.say("Stopped. :white_check_mark:")
        except:
            await client.say("The song is already stopped. :x:")
    else:
        return False

@client.command(pass_context=True)
async def leave(ctx):
    '''Bot leave the voice channel.'''
    if not ctx.message.author.bot:
        try:
            server = ctx.message.server
            voice_client = client.voice_client_in(server)
            await voice_client.disconnect()
            await client.say("I'm left the voice channel. :thumbsup:")
        except:
            await client.say("I'm not in a voice channel. :x:")
    else:
        return False


@client.command(aliases=['np'], pass_context=True)
async def now(ctx):
    if not ctx.message.author.bot:
        global playing
        await client.say(playing)
    else:
        return False

#-----------------------------------------------------Minigames-------------------------------------------------------------------#

@client.command(pass_context=True)
async def dice(ctx):
    await client.send_message(ctx.message.channel, random.choice([':game_die: Your number is **1**!',
                                            ":game_die: Your number is **2**!",
                                            ":game_die: Your number is **3**!",
                                            ":game_die: Your number is **4**!",
                                            ":game_die: Your number is **5**!",
                                            ":game_die: Your number is **6**!"]))

#------------------------------------------------------#-ed cmds------------------------------------------------------------------#

#@client.command(pass_context=True)
#async def sharp(ctx):
#    user == discord.utils.find(id='137977201344643072')
#    await client.send_message(user, "Hello Sam! :smile:\nThis is my file:")
#    await client.send_file(user, "VTUBot.py")



#@client.command(pass_context=True)
#async def emoji(ctx):
#    msg = await client.say("Yey! :smile:")
#    reactions = ['👍', '👎']
#    for emoji in reactions: 
#        await client.add_reaction(msg, emoji)


#@client.command(pass_context=True)
#async def roleinfo(self, ctx, role: discord.Role):
#    perm = (list(role.permissions))
#    embed=discord.Embed(color=role.color)
#    embed.add_field(name='__Role Info__', value='** **', inline=False)
#    embed.add_field(name='Rolename:', value='{0} | {1}'.format(role.name, role.mention), inline=True)
#    embed.add_field(name='Role ID:', value='{0}'.format(role.id), inline=True)
#    embed.add_field(name='Role color:', value='{0}'.format(role.color), inline=True)
#    embed.add_field(name='Role hoist:', value='{0}'.format(role.hoist), inline=True)
#    embed.add_field(name='Role position:', value='{0}'.format(role.position), inline=True)
#    embed.add_field(name='Role mentionable:', value='{0}'.format(role.mentionable), inline=True)
#    embed.add_field(name='Role permissions:', value='{0}'.format(perm), inline=True)
#    embed.add_field(name='Created at:', value='{0}'.format(role.created_at), inline=False)      
#    author = ctx.message.author
#    embed.set_footer(text='Message was requested by {0}'.format(author))
#    embed.timestamp = datetime.utcnow()
#    await self.client.send_message(ctx.message.channel, embed=embed)
#    embed.set_author(name="User Info", icon_url=user.avatar_url)


client.run(os.environ.get('TOKEN'))

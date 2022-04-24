import discord
import json
from discord.ext import commands, tasks
import urllib.request
import youtube_dl
import os
import time
import asyncio
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
from discord import TextChannel
from youtube_dl import YoutubeDL
app = commands.Bot(command_prefix="lb ", help_command=None)

def status():
    print("Turned On!")
@app.event
async def on_ready():
    print("Ready")
@app.command()
async def test(ctx):
    await ctx.channel.send("Frisbee is Online!")
@app.command()
async def weather(ctx, *, place):
    checkedString = place.replace(" ", "%20")
    apiKey = "2dbaf67dc49f21e173708c50813a0b23"
    emoji = ""
    url = f"http://api.weatherstack.com/current?access_key={apiKey}&query={checkedString}"
    with urllib.request.urlopen(url) as weather:
        data = json.loads(weather.read().decode())
    if "cloudy" in data['current']['weather_descriptions'][0].lower():
        emoji = ":cloud:"
    elif "sunny" in data['current']['weather_descriptions'][0].lower():
        emoji = ":sunny:"
    elif "clear" in data['current']['weather_descriptions'][0].lower():
        emoji = ":white_sun_cloud:"
    elif "rain" in data['current']['weather_descriptions'][0].lower():
        emoji = ":cloud_rain:"
    await ctx.channel.send(f"The current weather in {data['location']['name']} is {data['current']['temperature']}C")
    await ctx.channel.send(f"{data['current']['weather_descriptions'][0]} {emoji}")
@app.command()
async def time(ctx, option, region, *, location):
    checkedString = location.replace(" ", "_")
    if option.lower() == "get":
        with urllib.request.urlopen(f"https://www.timeapi.io/api/Time/current/zone?timeZone={region}/{checkedString}") as response:
            data = json.loads(response.read().decode())
        await ctx.channel.send(f"The current time in {data['timeZone']} is {data['hour']}:{data['minute']}:{data['seconds']}")
    elif option.lower() == "help":
        await ctx.channel.send("""
To use this command: 
    - Paremeters: fris (get/help) (region) (location) | For example: fris get Europe Amsterdam
    * Note: Place must have capitalized first letter
        """)
#music

# command for bot to join the channel of the user, if the bot has already joined and is in a different channel, it will move to the channel the user is in
@app.command()
async def play(ctx, option, *, keyword):
    url = ""
    #get youtube video
    if option == "search":
        checkedString = keyword.replace(" ", "%20")
        with urllib.request.urlopen(f'https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=20&q={checkedString}&type=video&key=AIzaSyAGHEd_NePDsBKt5yqhSyIiToQyJ7CNcw8') as yt:
            data = json.loads(yt.read().decode())
        url = "https://youtube.com/watch?v=" + str(data['items'][0]['id']['videoId'])
        name = data['items'][0]['snippet']['title']
    elif option == "url":
        url = keyword
    try:
        channel = ctx.message.author.voice.channel
        voice = get(app.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()
        YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
        FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

        if not get(app.voice_clients, guild=ctx.guild).is_playing():
            with YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(url, download=False)
            URL = info['url']
            get(app.voice_clients, guild=ctx.guild).play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
            get(app.voice_clients, guild=ctx.guild).is_playing()
            await ctx.send(f'LunarBot is playing {name} :musical_note:')
        else:
            await ctx.send("LunarBot is already playing")
            return
    except AttributeError:
        await ctx.send("You are not connected to a voice channel")
# check if the bot is already playing
    


# command to resume voice if it is paused
@app.command()
async def resume(ctx):
    if not get(app.voice_clients, guild=ctx.guild).is_playing():
        get(app.voice_clients, guild=ctx.guild).resume()
        await ctx.send('LunarBot is resuming')


# command to pause voice if it is playing
@app.command()
async def pause(ctx):
    if get(app.voice_clients, guild=ctx.guild).is_playing():
        get(app.voice_clients, guild=ctx.guild).pause()
        await ctx.send('LunarBot has been paused')


# command to stop voice
@app.command()
async def stop(ctx):
    if get(app.voice_clients, guild=ctx.guild).is_playing():
        await ctx.send('Stopping...')
        await get(app.voice_clients, guild=ctx.guild).disconnect()
app.run('OTY2OTUzODE3NjU0NTc5MjEw.YmJP6w.oiIM-Yx9UpXlUzsD7Yt9JqTjC30')
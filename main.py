import discord
from discord.ext import commands
import yt_dlp
import os

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Bot {bot.user} udah online!')

@bot.command()
async def play(ctx, *, search):
    if not ctx.author.voice:
        await ctx.send("Lu masuk VC dulu bg!")
        return
    vc = ctx.voice_client
    if not vc:
        vc = await ctx.author.voice.channel.connect()
    ydl_opts = {'format': 'bestaudio', 'noplaylist': True, 'quiet': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{search}", download=False)['entries'][0]
        url = info['url']
        title = info['title']
    vc.stop()
    vc.play(discord.FFmpegPCMAudio(url, before_options='-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'))
    await ctx.send(f"🎵 Lagi muter: **{title}**")

@bot.command()
async def skip(ctx):
    if ctx.voice_client:
        ctx.voice_client.stop()
        await ctx.send("Di-skip bg!")

@bot.command()
async def stop(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("Bot udah cabut!")

bot.run(os.getenv("DISCORD_TOKEN"))

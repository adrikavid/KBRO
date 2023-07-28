import discord
import asyncio
from discord.ext import commands
import youtube_dl
from pytube import YouTube

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.message_content = True


bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user.name} s'est connecté !")


@bot.command()
async def youtube(ctx, *, query):
    # Recherche de la vidéo sur YouTube
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts, verbose=True) as ydl:

        info = ydl.extract_info(f"ytsearch:{query}", download=False)
        if 'entries' in info:
            video_url = info['entries'][0]['webpage_url']
            yt = YouTube(video_url)
            audio_stream = yt.streams.filter(only_audio=True).first()
            if audio_stream:
                audio_url = audio_stream.url

                channel = ctx.author.voice.channel
                if not channel:
                    await ctx.send("Tu dois être dans un salon vocal pour utiliser cette commande.")
                    return

                voice_client = await channel.connect()
                voice_client.play(discord.FFmpegPCMAudio(audio_url), after=lambda e: print('done', e))

                await ctx.send(f"En train de jouer : {yt.title}")
                while voice_client.is_playing():
                    await asyncio.sleep(1)
                await voice_client.disconnect()
            else:
                await ctx.send(f"Impossible de trouver l'audio pour : {yt.title}")
        else:
            await ctx.send(f"Impossible de trouver la vidéo pour : {query}")

bot.run("")
bot.run("MTEzMTU1NzM5NjUzNjM4MTQ3Mg.Glu-Ms.j_YAC7d-vKS7CkyCFN420RZvLrk9w5lCUTH0Bs")
import speech_recognition as sr
from discord.ext import commands
from os import environ
from gtts import gTTS
from discord import PCMVolumeTransformer
from discord import FFmpegPCMAudio
from random import randint



bot = commands.Bot(
  command_prefix=commands.when_mentioned_or("<"),
  description="research bot @ https://github.com/JaffarA/dvc"
)


@bot.command()
async def hello(ctx):
  await ctx.send('hello world!')


@bot.command()
async def tts(ctx):
  """
  Plays a TTS message
  """
  txt = ctx.message.content.replace('<tts ', '')
  a, loc = gTTS(txt), f'tmp/{randint(690000, 6900000)}.mp3'
  a.save(loc)
  await join(ctx)
  s = PCMVolumeTransformer(FFmpegPCMAudio(loc))
  ctx.voice_client.play(s)
  await ctx.send(txt)


@bot.command()
async def listen(ctx):
  await join()
  r = sr.Recognizer()
  m = ctx.voice_client # todo

  def callback(recognizer, audio):
    try:
      print("Google Speech Recognition thinks you said",
            recognizer.recognize_google(audio))
    except sr.UnknownValueError:
      print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
      print("Could not request results from Google Speech Recognition service; {0}".format(e))

  with m as source:
    r.adjust_for_ambient_noise(source)
  stop_listening = r.listen_in_background(m, callback)


@bot.command()
async def join(ctx):
  """
  Joins a voice channel
  """
  channel = ctx.author.voice.channel

  if ctx.voice_client is not None:
    return await ctx.voice_client.move_to(channel)

  await channel.connect()

bot.run(environ["BOT_TOKEN"])

import discord #You'll need to install this
import random
import time
import subprocess #You'll need to install this and also download espeak and put in the same directory as this source code.
import threading
import os
import urllib.request
import json
from pathlib import Path
from datetime import datetime
from datetime import datetime,timedelta
#from dateutil.parser import parse

global player
global voice_client
global voice_channel
global old_voice_members

client = discord.Client()

def member_change():
  global old_voice_members
  global player
  if not (len(old_voice_members) == len(voice_channel.voice_members)):
    print("member change")
    if(len(old_voice_members) > len(voice_channel.voice_members)):
      print("Someone Left") #Someone left
      for i in range(0, len(old_voice_members)):
        if old_voice_members[i] not in voice_channel.voice_members:
          name = old_voice_members[i].display_name
          old_voice_members = []
          for k in range(0, len(voice_channel.voice_members)):
            old_voice_members.append(voice_channel.voice_members[k])
          if(name.startswith('(')):
            parindex = name.find(')')
            name = name[parindex+1:]
          file_name = "VoiceFiles/"+name+".wav"
          if Path(file_name).is_file():
            player = voice_client.create_ffmpeg_player(file_name)
            player.volume= 100/100 #Change the left number to adjust over all volume
            player.start()
            while(not player.is_done()):
              count = 0
            player = voice_client.create_ffmpeg_player("VoiceFiles/left.wav")
            player.volume= 100/100
            player.start()
            while(not player.is_done()):
              waitCount = 0
          else:
            textToWav(name,file_name)
            player = voice_client.create_ffmpeg_player("VoiceFiles/"+name+".wav")
            player.volume= 100/100
            player.start()
            while(not player.is_done()):
              waitCount = 0
            player = voice_client.create_ffmpeg_player("VoiceFiles/left.wav")
            player.volume= 100/100
            player.start()
            while(not player.is_done()):
              waitCount = 0
          break
      print("made it here")
    elif(len(voice_channel.voice_members) > len(old_voice_members)):
      print("Someone joined")
      for i in range(0, len(voice_channel.voice_members)):
        if voice_channel.voice_members[i] not in old_voice_members:
          name = voice_channel.voice_members[i].display_name
          old_voice_members = []
          for k in range(0, len(voice_channel.voice_members)):
            old_voice_members.append(voice_channel.voice_members[k])
          if(name.startswith('(')):
            parindex = name.find(')')
            name = name[parindex+1:]
          file_name = "VoiceFiles/"+name+".wav"
          if Path(file_name).is_file():
            player = voice_client.create_ffmpeg_player(file_name)
            player.volume= 100/100
            player.start()
            while(not player.is_done()):
              waitCount = 0
            player = voice_client.create_ffmpeg_player("VoiceFiles/joined.wav")
            player.volume= 100/100
            player.start()
            while(not player.is_done()):
              waitCount = 0
          else:
            textToWav(name,file_name)
            player = voice_client.create_ffmpeg_player("VoiceFiles/"+name+".wav")
            player.volume= 100/100
            player.start()
            while(not player.is_done()):
              waitCount = 0
            player = voice_client.create_ffmpeg_player("VoiceFiles/joined.wav")
            player.volume= 100/100
            player.start()
            while(not player.is_done()):
              waitCount = 0
          break
  threading.Timer(.5, member_change).start()


def textToWav(text, file_name):
  subprocess.call(["espeak", "-vf2", "-w"+file_name, text]) #Change (or remove) "f2" to a voice file in ~/espeak/espeak-data/voice to change the voice
  print("File written")

async def giphy_command(message):
  forbidden_gifs = ['/gamerescape', '/xivdb', '/giphy', '/tts', '/tenor', '/me', '/tableflip', '/unflip', '/shrug', '/nick']
  spaceIndex = message.content.find(' ')
  if message.content[:spaceIndex] in forbidden_gifs:
    return
  search_params = message.content[1:]
  search_params_sb = ""
  first = True
  for i in range(0,len(search_params)):
    if search_params[i] == ' ':
      search_params_sb = search_params_sb + search_params[len(search_params_sb):i] + '+'
  search_params_sb = search_params_sb + search_params[len(search_params_sb):]
  data = json.loads(urllib.request.urlopen('http://api.giphy.com/v1/gifs/search?q='+search_params_sb+'&api_key=API_KEY_HERE&limit=100').read()) #Add your own giphy API here key
  url = json.dumps(data["data"][random.randint(0,100)]["url"], sort_keys = True, indent = 4)
  await client.send_message(message.channel, url[1:len(url)-1])

async def join_voice(channel_id):
  global player
  global voice_client
  global voice_channel
  global old_voice_members
  voice_channel = client.get_channel(channel_id)
  voice = await client.join_voice_channel(voice_channel)
  player = voice.create_ffmpeg_player('VoiceFiles/init.wav')
  print("about to start playing")
  voice_client = voice
  old_voice_members = []
  for i in range(0, len(voice_channel.voice_members)):
    old_voice_members.append(voice_channel.voice_members[i])
  member_change()

async def ping_command(message):
  d = datetime.utcnow() - message.timestamp
  s = d.seconds*1000 + d.microseconds//1000
  await client.send_message(message.channel, "Ping: {}ms".format(s))

async def help_command(message):
  channel = message.channel
  help_message = """Here are list of available commands:
  < l+help >: *Displays a list of available commands*
  < l+status >: *Replys indicating I am online*
  < l+voice [channel_id] >: *Joins voice channel with specified Id (Special permissions required)*
  < l+ping >: *Responds with your ping*
  < l+stopvoice >: *Disconnects the bot from the current voice channel (Special permissions required)*
  < l+clean [amount] >: *Removes all messages from the channel this command was invoked in that were sent by me or that were commands for the me (Special permissions required)*
  < l+pizza >: *Just do it*
  < /[emote] >: Invoking a slash command will make me search for a relevant gif and then post it
  My main purpose on this server is to announce when users leave or join the voice channel I am in.
  Nibikk is the creator of me, contact him if you have any questions.
  Last updated 07/21/2017""" #Change the text here to customize your help message.
  await client.send_message(channel, help_message)

async def stop_voice(message):
  global voice_client
  await voice_client.disconnect()

async def reddit_link(message):
  await client.send_message(message.channel, "http://www.reddit.com"+message.content)

async def clean_command(message):
  channel = message.channel
  options = [channel, 50000, delete_message, message, None, None]
  await client.purge_from(channel, limit = 50000, check=lambda m: m.author.id == '335445369930514433' or m.content.startswith('l+'))

def delete_message(message):
  return False
  #if(message.author.id == '335445369930514433' or message.content.startswith('l+')):
   # return True

@client.event
async def on_ready():
    #info
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    if not os.path.exists("VoiceFiles"):
      os.makedirs("VoiceFiles")
    if( not (Path("VoiceFiles/joined.wav").is_file())):
      textToWav("Has joined the channel", "VoiceFiles/joined.wav")
    if( not (Path("VoiceFiles/left.wav").is_file())):
      textToWav("Has left the channel", "VoiceFiles/left.wav")
    if( not (Path("VoiceFiles/init.wav").is_file())):
      textToWav("init", "VoiceFiles/init.wav")
    print(len(client.messages))

@client.event
async def on_message(message):
  if(message.author l+= client.user):
    print(message.author.name + " said: \"" + message.content + "\" in #" + message.channel.name + " @ " + time.ctime())
  if(message.content.startswith('l+voice')):
    if(message.author.id == '159785058381725696' or message.author.id == '328175857707253760' or message.author.id == '314840626820677643' or message.author.id == '209415024354000897'): #These are user IDs and the logic only allows the players with this user ID to use this command
      if(len(message.content) < len('l+voice ')):
        await client.send_message(message.channel, 'Please provide a voice channel id')
        return
      channelId = message.content[len('l+voice '):]
      await client.send_message(message.channel, 'Joining voice channel with\nID: ' + channelId +'\nName: ' + client.get_channel(channelId).name)
      await join_voice(channelId)
      print("Joined voice channel with Id")
    else:
      count = 0
      await client.send_message(message.channel, "Sorry, you do not have permission to use this command. Please contact Nibikk if you have any questions.") #Change this line to yourself or simply "Bot Admin"
  elif(message.content.startswith('l+status')):
    await client.send_message(message.channel, 'I am here')
  elif(message.content.startswith('l+help')):
    await help_command(message)
  elif(message.content.startswith('l+ping')):
    await ping_command(message)
  elif(message.content.startswith('l+stopvoice')):
    if(message.author.id == '159785058381725696' or message.author.id == '328175857707253760'):
      await stop_voice(message)
  elif(message.content.startswith('/r/')):
    await reddit_link(message)
  elif(message.content.startswith('l+clean')):
    if(message.author.id == '159785058381725696' or message.author.id == '328175857707253760'):
      await clean_command(message)
    else:
      await client.send_message('Sorry, you do not have permission to use this command. Please contact Nibikk if you have any questions.')
  elif(message.content.startswith('l+pizza')):
    await client.send_message(message.channel, 'The fuck you think I am? Think I can order you pizza? Who\'s paying for this shit?')
  elif(message.content.startswith('l+Mugglewump')):
    if(message.author.id == '159785058381725696' or message.author.id == '83809782691004416'):
      await client.send_message(message.channel, '<@328175857707253760> is a dope Templarl+')
  elif(message.content.startswith('/')):
    await giphy_command(message)

client.run('NDQ3NDAxMTIyNTAwNTc1MjMz.DfsxOw.Ra8xWT5jeB0aTSFCdy4Q2B14gPA') #Add your own bot's token here

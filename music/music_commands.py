import discord
from discord import VoiceChannel as vc
from discord.ext.commands import Bot
from youtube_dl import YoutubeDL
import YTDLsource
import music as m
from song import Song
import config


SECRET_KEY = config.KEY #Replace 'config.key' with your key

bot = Bot(command_prefix = '?')
music_player = None #This shouldn't be a global

#For testing purposes. It will be removed
@bot.event
async def on_ready():
	print('Bot is running')


@bot.group(name = 'music', invoke_without_command = True)
async def music(ctx):
	await ctx.send("oof")


@music.command(name= 'queue')
async def queue(ctx):
	if not music_player or music_player.queue_is_empty():
		await ctx.send("The queue is currently empty. Feel free to add some cool jams!")
		return

	await ctx.send("Some music")


@music.command(name = 'play')
async def play(ctx, *, args):
	print(args)
	try:
		voice_channel = get_voice_channel(ctx, ctx.message.author)
	except TypeError:
		await ctx.send(ctx.message.author.mention + " You must be in a voice channel if you want to headbang bro")
		return

	if not await bot_connected(voice_channel):
		global music_player 
		music_player = m.Music(ctx)

	data_source, data = await ytsource.create_source(args)
	source = discord.FFmpegPCMAudio(data_source)

	#song = Song(data)
	await music_player.add_to_queue(source, data['title'])
	#await ctx.send(embed=song.create_embed())


@music.command(name = 'stop')
async def stop(ctx):
	vc = ctx.voice_client

	if not vc or not vc.is_connected():
		return await ctx.send('I\'m not playing any song at the moment', delete_after=10)

	try:
		await ctx.guild.voice_client.disconnect() #Implement this on Music class
	except AttributeError:
		pass

"""
Checks if a bot is connected to a certain voice channel. 
If it isn't, then an attempt at connecting will be made

@param voice_channel VoiceChannel we're trying to connect to
@return a boolean value	-	True if the bot is already connected
						-	False if it isn't connected
"""
async def bot_connected(voice_channel):
	try:
		await voice_channel.connect()
		return False
	except discord.ClientException:
		return True


"""
@param ctx Current context
@param user The Member that sent the message
@return VoiceChannel, if the user is at a Voice Channel
@throws TypeError if the user isn't at a Voice Channel
"""
def get_voice_channel(ctx, user):
	for channel in bot.get_all_channels():
		if channel.type is discord.ChannelType.voice and user in channel.members:
			return channel
	raise TypeError

ytsource = YTDLsource.YTDLsource()
bot.run(SECRET_KEY)
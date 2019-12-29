import discord
from discord import VoiceChannel as vc
from discord.ext.commands import Bot
import YTDLsource
import music as m
from song import Song
import config


SECRET_KEY = config.KEY #Replace 'config.key' with your key

bot = Bot(command_prefix = '?')


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
	try:
		voice_channel = get_voice_channel(ctx, ctx.message.author)
	except TypeError:
		await ctx.send(ctx.message.author.mention + 
					" You must be in a voice channel if you want to headbang bro")
		return

	if not await bot_connected(voice_channel):
		global music_player 
		music_player = m.Music(ctx)

	data_source, data = await ytsource.create_source(args)
	song = Song(data)
	data['file_path'] = data_source
	data['requester'] = ctx.message.author
	await music_player.add_to_queue(discord.FFmpegPCMAudio(data_source), data)


@music.command(name = 'stop')
async def stop(ctx):
	vc = ctx.voice_client

	if not vc or not vc.is_connected():
		return await ctx.send('I\'m not playing any song at the moment', delete_after=10)

	try:
		global music_player
		await ctx.guild.voice_client.disconnect() #Implement this on Music class
		await music_player.stop_queue_loop()
		music_player.cleanup()
		music_player = None
	except AttributeError:
		pass


"""
If the VoiceClient is playing audio, then the audio is paused
@param ctx Current context
"""
@music.command(name  = 'pause')
async def pause(ctx):
	vc = ctx.voice_client
	if vc and vc.is_playing():
		vc.pause()


"""
If the VoiceClient is playing audio, but is paused then the audio is resumed.
@param ctx Current context
"""
@music.command(name = 'resume')
async def resume(ctx):
	vc = ctx.voice_client
	if vc and vc.is_paused():
		vc.resume()


"""
If the VoiceClient is playing audio, a visual representation of the current song
will be presented on the channel where the command was invoked.
@param ctx Current context
"""
@music.command(name = 'current')
async def current(ctx):
	vc = ctx.voice_client
	if vc and vc.is_playing and music_player:
		await ctx.send(embed=music_player.get_current_song())


"""
Checks if a bot is connected to a certain voice channel. 
If it isn't, then an attempt at connecting will be made

@param voice_channel VoiceChannel we're trying to connect to
@return a boolean value	-	True if the bot is already connected
						-	False if it isn't connected
"""
async def bot_connected(voice_channel):
	try:
		await voice_channel.connect(reconnect = True)
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


music_player = None #This shouldn't be a global
ytsource = YTDLsource.YTDLsource()
try:
	bot.run(SECRET_KEY)
except KeyboardInterrupt:
	print('Bot is shutting down.')
import discord

class Song():
	
	"""
	@param data a dictionary containing relevant information 
				to create a visual representation of the song
	"""
	def __init__(self, data):
		self.data = data


	"""
	This method will be used for a visual representation of the queue
	"""
	def create_embed(self, song_queue=None):

		embed = (discord.Embed(title='Now playing',
							color=discord.Color.blurple())
				.add_field(name="Title", value=self.data['title'])
				.add_field(name="Requested by", value=self.data['requester'])
				.add_field(name='Duration', value=self.data['duration'])
				.set_thumbnail(url=self.data['thumbnail']))
		
		if not song_queue or len(song_queue) == 1:
			return embed

		embed.add_field(name='__**Up next**__', value= '\a' )
		i = 1
		for song in song_queue[1:]:
			embed.add_field(name=str(i), value=song.data['title'] + ' | `' + song.data['duration'] + ' | Requested by: ' + str(song.data['requester']) + '`', inline=False)
			i += 1

		return embed
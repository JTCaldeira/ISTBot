class Song():
	"""
	TODO reduce the data being passed
	"""
	def __init__(self, data):
		self.data = data


	"""
	This method will be used for a visual representation of the queue
	"""
	def create_embed(self):
		embed = (discord.Embed(title='Now playing',
								color=discord.Color.blurple())
				 .add_field(name='Duration', value=self.data['duration']))

		return embed


		#				 .add_field(name='Requested by', value=self.requester.mention)

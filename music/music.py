import asyncio
from async_timeout import timeout
import os

class Music():
	def __init__(self, ctx):
		self.bot = ctx.bot
		self.guild = ctx.guild
		self.queue = asyncio.Queue()
		self.next = asyncio.Event()
		self.current_song = None
		self.DOWNLOAD_DIRECTORY = 'downloads/'

		ctx.bot.loop.create_task(self.queue_loop())


	def get_queue(self):
		return self.queue


	def queue_is_empty(self):
		return self.queue.empty()


	async def add_to_queue(self, song, title):
		await self.queue.put([song, title])


	def pop_queue_element(self):
		self.queue.get()


	def remove_download_file(self, file_name):
		file_path = self.DOWNLOAD_DIRECTORY + file_name
		print(file_path)
		if os.path.exists(file_path):
			os.remove(file_path)
		else:
			print("The file doesn't exist") #Might be better to just handle the exception here


	async def queue_loop(self):

		await self.bot.wait_until_ready()

		while not self.bot.is_closed():
			self.next.clear()

			try:
				async with timeout(300):
					source, title = await self.queue.get()
			except asyncio.TimeoutError:
				return

			self.current_song = source

			self.guild.voice_client.play(source, after=lambda _: self.bot.loop.call_soon_threadsafe(self.next.set))

			await self.next.wait()
			self.remove_download_file(title.replace(' ', '_').replace('\'', '_')) #pls god no

			source.cleanup()
			self.current_song = None


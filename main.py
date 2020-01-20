from discord.ext.commands import Bot
from discord.ext.commands import errors
import config


def instantiate_bot():
	bot = Bot(command_prefix = '?')

	files = ('music.music_commands',)

	for file in files:
		try:
			bot.load_extension(file)
		except errors.ExtensionNotFound:
			print(f'Failed to find the extension {file}.')

	try:
		bot.run(config.SECRET_KEY)
		print('Bot is running.')
	except KeyboardInterrupt:
		print('Bot is shutting down.')


if __name__ == "__main__":
	instantiate_bot()
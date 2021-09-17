from env import BOT_TOKEN
from discord.ext import commands
from bot.Player import Player

bot = commands.Bot(command_prefix=commands.when_mentioned_or('.ava '),
                   description='Best discord music bot')


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} ({bot.user.id})')
    print('------')

bot.add_cog(Player(bot))


def run():
    bot.run(BOT_TOKEN)

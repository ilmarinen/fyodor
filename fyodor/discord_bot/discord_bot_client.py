import discord
import os
import re
from fyodor.discord_bot import commands



class DiscordBotClient(object):

    def __init__(self, client_id=None):
        self.client = discord.Client()
        self.command_dispatcher = commands.Dispatcher()

        def is_mentioned(message, client_id):
            return client_id in [mention.id for mention in message.mentions]

        @self.client.event
        async def on_ready():
            print('We have logged in as {0.user}'.format(self.client))

        @self.client.event
        async def on_message(message):
            if message.author == self.client.user:
                return

            if is_mentioned(message, client_id):
                command_text_matcher = re.compile(f"\<\@\!{client_id}\>(.+)")
                command_relevant_text = command_text_matcher.match(message.content).group(1)
                embeds = self.command_dispatcher.process_any_commands(message, command_relevant_text)
                for embed in embeds:
                    await message.channel.send(embed=embed)

    def run(self, token):
        self.client.run(token)

import datetime
import discord
from fyodor import scrapers


def get_batched_headlines(source, batch_size):
    headlines = source.get_headlines()
    if len(headlines) > 0:
        embeds = []
        if len(headlines) < 5:
            headlines_batch = headlines
            current_datetime_string = datetime.datetime.now().strftime("%a, %B %d, %Y")
            headlines_string = "\n\n".join(map(lambda h: h["title"], headlines_batch))
            embed = discord.Embed(title=f"{current_datetime_string} Headlines ({source.name})", description=headlines_string)
            embeds.append(embed)
        else:
            for i in range(int(len(headlines) / batch_size)):
                k = 5 * i
                headlines_batch = headlines[k:(k + batch_size)]
                current_datetime_string = datetime.datetime.now().strftime("%a, %B %d, %Y")
                headlines_string = "\n\n".join(map(lambda h: h["title"], headlines_batch))
                embed = discord.Embed(title=f"{current_datetime_string} Headlines ({source.name})", description=headlines_string)
                embeds.append(embed)

        return embeds


class Dispatcher(object):

    def __init__(self):
        self.news_sources = dict()
        self.news_sources["wikipedia"] = scrapers.WikipediaScraper()
        self.news_sources["cnbc"] = scrapers.CNBCScraper()

    def process_any_commands(self, message, command_text):
        command_words = list(filter(lambda word: len(word) > 0, command_text.strip().split(" ")))
        if len(command_words) == 0:
            print("No commands found.")

        command_string = command_words[0]
        command_parameters = command_words[1:]

        if len(command_parameters) == 0:
            return []

        if command_string == "headlines" and command_parameters[0] not in ["list", "all"]:
            source_name = command_parameters[0].lower()
            source = self.news_sources[source_name]
            headlines = source.get_headlines()
            embeds = get_batched_headlines(source, 5)

            return embeds

        elif command_string == "list" and command_parameters[0] == "sources":
            news_sources_string = "\n\n".join(self.news_sources.keys())
            embed = discord.Embed(title=f"Available News Sources", description=news_sources_string)

            return [embed]

        elif command_string == "headlines" and command_parameters[0] == "all":
            embeds = []
            for _, source in self.news_sources.items():
                source_embeds = get_batched_headlines(source, 5)
                embeds = embeds + source_embeds

            return embeds

        return []

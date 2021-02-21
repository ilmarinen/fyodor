import os
import click
import requests
import urllib.request
from bs4 import BeautifulSoup
from fyodor.discord_bot import DiscordBotClient


@click.group()
def cli():
    pass


@cli.command(name="discord-bot")
def run_discord_bot():
    """
    This command starts a Discord bot, that connects to a channel and starts
    listening for commands.
    """

    client_id = int(os.getenv("CLIENT_ID"))
    bot_client = DiscordBotClient(client_id=client_id)
    bot_client.run(os.getenv("TOKEN"))


@cli.command(name="scrape")
@click.option("-u", "--url", default=None, required=True)
def scrape(url):
    """
    This command perturbes the detected genders of persons in the sentence.
    Changing male persons to female, and female persons to male.
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    divs = soup.select("div")

    print(divs)


def main():
    cli()

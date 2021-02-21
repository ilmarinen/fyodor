# Fyodor

## Installation and Running

1. To install it, run the following command within the top level of the repo: `pip install -e .`
2. Once installation is complete you will need a `Token` and `Client Id` for your Bot. Follow the instructions (here)[https://www.freecodecamp.org/news/create-a-discord-bot-with-python/].
3. Then set two environment variables `TOKEN` and `CLIENT_ID` to be the values of your token and client id.
4. Run the command: `fyodor discord-bot`
5. Alternately on Linux you can run: `CLIENT_ID=<your-client-id> TOKEN=<your-token> fyodor discord-bot`

## Discord

You can interact with Fyodor on Discord by mentioning them and sending them a command.

1. Ask for a list of available news sources: `@Fyodor list sources`
2. Ask for the headlines from a particular source: `@Fyodor headlines <source-name>`
3. Ask for the headlines from all sources: `@Fyodor headlines all`

import discord
from bot_token import TOKEN
from random import randint

from markov import TimeHomog, TextParser
MINGEN = 12
MAXGEN = 48


def find_key(msg: str) -> bool:
    keys = ["dagoth", "n'wah", "nwah", "s'wit", "swit", "sixth", "house",
            "nerevar", "farm", "tools", "argonians", "dunmer", "dark elf"]

    string_arr = msg.split(" ")
    for i in range(len(string_arr)):
        string_arr[i].lower()

    for key in keys:
        if key in string_arr:
            return True

    return False


class BotEntity:
    def __init__(self, client, markov: TimeHomog):
        self.client = client
        self.markov = markov
        self.client.event(self.on_ready)
        self.client.event(self.on_message)

    async def on_ready(self):
        print(f'Logged in as {client.user}')

    async def on_message(self, msg):
        if msg.author == client.user:
            return

        if find_key(msg.content):
            await msg.channel.send(
                f'{msg.author}, {self.markov.generate(None, randint(MINGEN, MAXGEN))}')


if __name__ == "__main__":
    intents = discord.Intents.default()
    intents.messages = True
    intents.message_content = True
    client = discord.Client(intents=intents)

    parser = TextParser()
    markov = TimeHomog(parser.get_words())

    bot = BotEntity(client, markov)
    client.run(TOKEN)

import discord
import bot_token
import generate as resp

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

client = discord.Client(intents=intents)

words = []


def find_key(msg: str) -> bool:
    key = "dagoth"
    string_arr = msg.split(" ")

    for item in string_arr:
        if item == key:
            return True

    return False


@client.event
async def on_ready():
    words.clear()
    print(f'Logged in as {client.user}')
    tmp = resp.build_list(resp.clean_text(resp.read_file("dagoth.txt")))
    for i in range(len(tmp)):
        words.append(tmp[i])


@client.event
async def on_message(msg):
    if msg.author == client.user:
        return

    if find_key(msg.content):
        await msg.channel.send(f'{msg.author}, {resp.resp_gen(words)}')

client.run(bot_token.TOKEN)

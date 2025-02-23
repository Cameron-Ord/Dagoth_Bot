import discord
import bot_token
import generate as resp
import copy

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

client = discord.Client(intents=intents)


class ListTracker:
    def __init__(self):
        self.words: list[dict[str, list[float]]] = []

    def replace(self, mutation: list[dict[str, list[float]]]):
        self.clear_words()
        self.modify_words(mutation)

    def get_words(self):
        return self.words

    def clear_words(self):
        self.words.clear()

    def modify_words(self, mutation: list[dict[str, list[float]]]):
        self.words = copy.deepcopy(mutation)


class EventTracker:
    def __init__(self):
        self.event_counter: int = 0

    def get_count(self) -> int:
        return self.event_counter

    def increment(self):
        self.event_counter += 1

    def reset(self):
        self.event_counter = 0


event_tracker = EventTracker()
ltrck = ListTracker()


def find_key(msg: str) -> bool:
    key = "dagoth"
    string_arr = msg.split(" ")

    for item in string_arr:
        if item == key:
            return True

    return False


@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    ltrck.replace(resp.build_list(
        resp.clean_text(resp.read_file("dagoth.txt"))))


@client.event
async def on_message(msg):
    if msg.author == client.user:
        return

    if event_tracker.get_count() >= 4:
        ltrck.replace(resp.reset_weights(ltrck.get_words()))
        event_tracker.reset()

    if find_key(msg.content):
        await msg.channel.send(f'{msg.author}, {resp.resp_gen(ltrck.get_words())}')
        event_tracker.increment()

client.run(bot_token.TOKEN)

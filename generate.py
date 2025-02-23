import random


NPREF: int = 4
MINGEN: int = 12
MAXGEN: int = 24
NOWWORD: str = "\n"

weight_count: int = 128


def build_list(words: list[str]) -> list[dict[str, list[float]]]:
    weighted = []
    for i in range(len(words)):
        weights = []
        for j in range(weight_count):
            weights.append(random.uniform(0.0125, 0.0175))

        item = {'word': words[i].lower(), 'weight': weights}
        weighted.append(item)

    return weighted


def clean_text(words: list[str]) -> list[str]:
    seen = set()
    unique = []

    for word in words:
        if word == NOWWORD:
            seen.add(word)
            continue

        if word not in seen:
            unique.append(word.strip())
            seen.add(word)

    return unique


def read_file(fp: str) -> list[str]:
    with open(fp, 'r') as file:
        return file.read().split(',')


def wrap(pos: int, increm: int, len: int) -> int:
    return (pos + increm) % len


def next_word(mat: dict[str, list[float]], temp: float) -> int:
    r: float = random.random()
    sum: float = 0.0
    offset: int = random.randint(0, weight_count-1)

    for i in range(0, weight_count):
        sum += (mat['weight'][wrap(i, offset, weight_count)] + temp)
        if r <= sum:
            return i
        else:
            continue


def resp_gen(words: list[dict[str, list[float]]]) -> str:
    last_word: list[str] = []
    response: str = ""
    nwords: int = random.randint(MINGEN, MAXGEN)
    pos: int = random.randint(0, len(words) - 1)

    for i in range(nwords):
        temp = random.uniform(random.uniform(-0.00250, -0.00125),
                              random.uniform(0.00125, 0.00250))

        word: str = words[pos]['word']
        pos = wrap(pos, next_word(words[pos], temp), len(words))

        next: bool = False
        for j in range(len(last_word)):
            if word == last_word[j]:
                next = True

        if next:
            continue

        response += word + " "
        last_word.append(word)

        if (len(last_word) > NPREF):
            last_word.pop(0)

    return response

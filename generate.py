import random


NPREF: int = 8
MINGEN: int = 4
MAXGEN: int = 32
NOWWORD: str = "\n"

weight_count: int = 32


def build_list(words: list[str]) -> list[dict[str, list[float]]]:
    weighted = []
    for i in range(len(words)):
        weights = []
        for j in range(weight_count):
            weights.append(random.uniform(0.25, 0.5))

        item = {'word': words[i].lower(), 'weight': weights}
        weighted.append(item)

    return weighted


def clean_text(words: list[str]) -> list[str]:
    seen = set()
    unique = []

    for word in words:
        if word.strip() not in seen:
            unique.append(word.strip())
            seen.add(word.strip())

    return unique


def read_file(fp: str) -> list[str]:
    with open(fp, 'r') as file:
        return file.read().split(',')


def wrap(pos: int, increm: int, len: int) -> int:
    return (pos + increm) % len


def next_word(mat: dict[str, list[float]]) -> int:
    r: float = random.random()
    sum: float = 0.0
    offset: int = random.randint(0, weight_count-1)

    for i in range(0, weight_count):
        sum += (mat['weight'][wrap(i, offset, weight_count)])
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
        word: str = words[pos]['word']
        pos = wrap(pos, next_word(words[pos]), len(words))

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

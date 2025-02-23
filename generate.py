import random
import copy


NPREF: int = 3
MINGEN: int = 4
MAXGEN: int = 32
NOWWORD: str = "\n"

weight_count: int = 4


def reset_weights(words: list[dict[str, list[float]]]):
    words_cpy = copy.deepcopy(words)
    for i in range(len(words_cpy)):
        for j in range(len(words_cpy[i]['weight'])):
            words_cpy[i]['weight'][j] = round(random.uniform(0.25, 0.5), 4)
    return words_cpy


def build_list(words: list[str]) -> list[dict[str, list[float]]]:
    weighted = []
    for i in range(len(words)):
        weights = []
        for j in range(weight_count):
            weights.append(round(random.uniform(0.25, 0.5), 4))

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
        variance = round(random.uniform(-0.05, 0.05), 4)
        sum += (mat['weight'][wrap(i, offset, weight_count)] + variance)
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

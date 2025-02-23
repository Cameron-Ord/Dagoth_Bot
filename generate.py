import random
import funny
from funny import funny_word, funny_standin


NPREF: int = 2
MINGEN: int = 12
MAXGEN: int = 24
NOWWORD: str = "\n"


def add(prefix: list[str], suffix: str):
    return {'word': suffix, 'pfx': [prefix[0], prefix[1]]}


def build_list(prefix: list[str], words: list[str]) -> list[dict[str, list[str]]]:
    arr = []
    for i in range(len(words)):
        arr.append(add(prefix, words[i].lower()))
        prefix[1:]
        prefix.append(words[i].lower())

    arr.append(add(prefix, NOWWORD))
    return arr


def clean_text(words: list[str]) -> list[str]:
    seen = set()
    unique = []

    for word in words:
        if word not in seen:
            unique.append(word.strip())
            seen.add(word)

    return unique


def read_file(fp: str) -> list[str]:
    with open(fp, 'r') as file:
        return file.read().split(',')


def find(prefix: str, words: list[dict[str, list[str]]]) -> int:
    for i in range(len(words)):
        pfx = words[i]['pfx']
        j: int = 0
        while (j < NPREF):
            if pfx[j] != prefix[j]:
                break
            j += 1
        if j == NPREF:
            return i


def resp_gen(words: list[dict[str, list[str]]]) -> str:
    prefix = [NOWWORD, NOWWORD]
    response = ""
    for i in range(random.randint(MINGEN, MAXGEN)):
        word = ""
        pos: int = find(prefix, words)
        nmatch: int = 0

        for j in range(pos, len(words)):
            nmatch += 1
            if random.randint(0, nmatch - 1) == 0:
                word = words[j]['word']

        if word == NOWWORD:
            break

        prefix[1:]
        prefix.append(word)

        if word == funny_word:
            word == funny_standin

        response += word + " "

    return response

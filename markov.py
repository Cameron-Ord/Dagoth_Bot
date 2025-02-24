import random


class TextParser:
    def __init__(self):
        self.fp = "dagoth.txt"
        self.words = []
        self.contents = self.process_text()

    def process_text(self):
        with open(self.fp, 'r') as file:
            self.contents = file.read().strip()
        tmp: list[str] = self.contents.split(',')
        for word in tmp:
            self.words.append(word.lower())

    def get_words(self):
        return self.words


class TimeHomog:
    def __init__(self, word_arr: list[str]):
        self.matrix = self.build_matrix(word_arr)
        self.states = list(self.matrix.keys())

    def generate(self, start_word=None, length=10):
        if len(self.states) == 0:
            return ""

        start_word = random.choice(self.states)
        sentence = [start_word]
        current_word = start_word

        for _ in range(length - 1):
            if current_word not in self.matrix:
                break

            if len(self.matrix[current_word]) == 0:
                break

            next_words = list(self.matrix[current_word].keys())
            probabilities = list(self.matrix[current_word].values())
            next_word = random.choices(next_words, weights=probabilities)[0]

            sentence.append(next_word)
            current_word = next_word

        return " ".join(sentence) + "."

    def build_matrix(self, words: list[str]):
        # Initialize matrix
        matrix = {}
        for word in words:
            if word not in matrix:
                # Add word with empty key:value {'word':{}, 'word':{}, ...}
                matrix[word] = {}

        for i in range(len(words) - 1):
            # Get the current and next word
            current_word = words[i]
            next_word = words[i+1]

            # Assign the next word key:value to the current object
            if next_word in matrix[current_word]:
                matrix[current_word][next_word] += 1
            else:
                # This will place it initially with a 1 default value
                # {'word':{'next_word': 1}, 'word':{'next_word': 1}, ...}
                matrix[current_word][next_word] = 1

        for current_word in matrix:
            # Sum values
            total = sum(matrix[current_word].values())
            for next_word in matrix[current_word]:
                # Normalize values
                matrix[current_word][next_word] /= total

        return matrix

import string
import sys
words = {}
strip = string.whitespace + string.punctuation + string.digits + "\"'"
filename = 'training.en'
for line in open(filename):
    for word in line.lower().split():
        word = word.strip(strip)
        if len(word) > 2:
            words[word] = words.get(word, 0) + 1
for word in sorted(words):
    print("'{0}' vstrechaetsia {1} raz".format(word, words[word]))

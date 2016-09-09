"""Wordcount exercise
Google's Python class

The main() below is already defined and complete. It calls print_words()
and print_top() functions which you write.

1. For the --count flag, implement a print_words(filename) function that counts
how often each word appears in the text and prints:
word1 count1
word2 count2
...

Print the above list in order sorted by word (python will sort punctuation to
come before letters -- that's fine). Store all the words as lowercase,
so 'The' and 'the' count as the same word.

2. For the --topcount flag, implement a print_top(filename) which is similar
to print_words() but which prints just the top 20 most common words sorted
so the most common word is first, then the next most common, and so on.

Use str.split() (no arguments) to split on all whitespace.

Workflow: don't build the whole program at once. Get it to an intermediate
milestone and print your data structure and sys.exit(0).
When that's working, try for the next milestone.

Optional: define a helper function to avoid code duplication inside
print_words() and print_top().

"""

import sys

def read_words(filename):
    words = []
    with open(filename, "r") as f:
        for line in f:
            words.extend(line.split())
    return words


def calc_words(filename):
    words = read_words(filename)
    words = list(map(lambda x: x.lower(), words))
    s = set(words)
    d = dict(zip(s, [0] * len(s)))
    for i in range(len(words)):
        d[words[i]] += 1
    return d


def print_words(filename):
    d = calc_words(filename)
    sorted_d = sorted(zip(d.keys(), d.values()))
    for i in range(len(sorted_d)):
        print(sorted_d[i][0], sorted_d[i][1])

#if there are several words with the same count in top 20, they will be sorted by word inside this groups

def print_top(filename):
    d = calc_words(filename)
    sorted_d = sorted(zip(d.values(), d.keys()), key = lambda x:(-x[0], x[1]))
    for i in range(min(len(sorted_d), 20)):
        print(sorted_d[i][1], sorted_d[i][0])


###

# This basic command line argument parsing code is provided and
# calls the print_words() and print_top() functions which you must define.
def main():
    if len(sys.argv) != 3:
        print('usage: ./wordcount.py {--count | --topcount} file')
        sys.exit(1)

    option = sys.argv[1]
    filename = sys.argv[2]
    if option == '--count':
        print_words(filename)
    elif option == '--topcount':
        print_top(filename)
    else:
        print('unknown option: ' + option)
        sys.exit(1)

if __name__ == '__main__':
    main()

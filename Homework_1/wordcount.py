import sys

def read_words(filename):
    words = []
    with open(filename, "r") as f:
        for line in f:
            words.extend(line.split())
    return words


def calc_words(filename):
    words = read_words(filename)
    words = [x.lower() for x in words]
    #ifsdf
    d = dict.fromkeys(words, 0)
    for i in range(len(words)):
        d[words[i]] += 1
    return d


def print_words(filename):
    d = calc_words(filename)
    sorted_d = sorted(d.items())
    for word, count in sorted_d:
        print(word, count)

#if there are several words with the same count in top 20, they will be sorted by word inside this groups

def print_top(filename):
    d = calc_words(filename)
    sorted_d = sorted(zip(d.values(), d.keys()), key = lambda x:(-x[0], x[1]))
    for count, word in sorted_d[:20]:
        print(word, count)


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
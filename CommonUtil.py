# http://en.wiktionary.org/wiki/Category:English_swear_words
swear_words = {"arse", "ass", "asshole", "bastard", "bitch", "bloody", "bollocks", "child-fucker",
               "Christ on a bike", "Christ on a cracker", "cunt", "damn", "fuck", "goddamn", "godsdamn"
               "hell", "holy shit", "Jesus", "Jesus Christ", "Jesus H. Christ", "Jesus Harold Christ",
               "Jesus wept", "Jesus, Mary and Joseph", "Judas Priest", "motherfucker",  "shit"
               "shit ass", "shitass", "son of a bitch", "son of a motherless goat", "son of a whore",
               "sweet Jesus"}


def count_unique_chars(inp):
    d = {}
    for letter in inp:
        if letter in d:
            count = d[letter]+1
            d[letter] = count+1
        else:
            d[letter] = 1
    return d.keys().__len__()


def count_swear_words(inp):
    count = 0
    for swear_word in swear_words:
        if swear_word.lower() in inp.lower():
            count += 1
    return count
print count_swear_words("Test")


def file_len(fname):
    cnt = 0
    with open(fname) as f:
        for i, l in enumerate(f):
           cnt += 1
    return cnt
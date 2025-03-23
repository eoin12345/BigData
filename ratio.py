from lists_of_chars import vowels, ignore, fillers


def calculate_vcr_for_pair(pair):
    return (pair[1], calculate_vcr(pair[0]))


def remove_filler(word):
    if not word or type(word) == float:
        return None
    for c in word:
        if c in fillers:
            word = word.replace(c, "")
    if len(word) == 0:
        return None

    return word


def remove_filler_for_pair(word):
    return (remove_filler(word[0]), word[1])


def calculate_vcr(word):
    vc = 0
    ignored = 0
    for c in word:
        if c in vowels:
            vc += 1
        if c in ignore:
            ignored += 1

    return vc / (len(word) - ignored)

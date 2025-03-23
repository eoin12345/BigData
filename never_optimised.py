import pandas as pd
from lists_of_chars import frequencies


def add_to_language_df(df, country, language_df):
    language_df = language_df._append(
        df[["word"]].assign(language=country), ignore_index=True
    )
    return language_df


def add_csv(file, country, delim, word_column, language_df, header=True):
    if header:
        df = pd.read_csv(file, delimiter=delim)
    else:
        df = pd.read_csv(file, delimiter=delim, header=None)

    df["word"] = df[word_column]
    return add_to_language_df(df, country, language_df)


def add_json(file, country, line, language_df):
    df = pd.read_json(file, lines=line)

    if "classification" in df.columns:
        df = df[df["classification"].str.contains("conjugaci") == False]
    else:
        df = df[df["definition"].str.contains("plural") == False]

    return add_to_language_df(df, country, language_df)


def add_russian_df(language_df):
    file_name = "data/dictionary.txt"
    russian_df = set()
    with open(file_name) as file:
        get = False
        for line in file.read().split("\n"):
            if get and len(line.split("\t")) > 1:
                word = line.split("\t")[0].strip()
                russian_df.add(word)
                get = False

            elif len(line.split()) == 1 and line.strip().isdigit():
                get = True

    russian_df = pd.DataFrame(russian_df, columns=["word"])
    return add_to_language_df(russian_df, "Russia", language_df)


def make_temperature_df():
    file_name = "data/city_temperature.csv"
    with open(file_name) as file:
        df = pd.read_csv(file)
        df = df[df["AvgTemperature"] != -99]
        country_avg_temperature_df = df.groupby("Country")["AvgTemperature"].mean()
        country_avg_temperature_df = country_avg_temperature_df.apply(
            lambda x: (x - 32) * 5 / 9
        )
    return country_avg_temperature_df


countries = list(frequencies.keys())
countries += [
    "France",
    "United Kingdom",
    "Poland",
    "Germany",
    "Spain",
    "Italy",
    "Russia",
]


def make_big_countries():

    language_df = pd.DataFrame(columns=["word", "language"]).astype("string")

    language_df = add_csv(
        "data/unigram_freq.csv", "United Kingdom", ",", "word", language_df
    )
    language_df = add_csv("data/osps37.txt", "Poland", "\t", "aa (ndm)", language_df)
    language_df = add_csv("data/de_word_ipa.csv", "Germany", ",", "words", language_df)
    language_df = add_csv("data/Lexique383.tsv", "France", "\t", "lemme", language_df)
    language_df = add_json("data/train.jsonl", "Spain", True, language_df)
    language_df = add_json("data/dictionary_sorted.json", "Italy", False, language_df)
    language_df = add_russian_df(language_df)
    return language_df

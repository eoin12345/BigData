import pandas as pd

from ratio import calculate_vcr, remove_filler
from lists_of_chars import frequencies
from scatter import scatter
from never_optimised import countries, make_temperature_df, make_big_countries
from benchmarker import MemoryTracker

memory = MemoryTracker("Unoptimised python")
computation_tracker = MemoryTracker("Computations")

if __name__ == "__main__":

    temperature_dic = {}
    vcr_dic = {}

    memory.start("Big countries")
    language_df = make_big_countries()
    memory.end()

    memory.start("Temperature")
    country_avg_temperature_df = make_temperature_df()
    memory.end()

    computation_tracker.start("Not optimised")
    memory.start("Small countries")
    for country, short in frequencies.items():
        words = {}
        with open("data/" + short + "_full.txt") as f:
            for line in f.read().splitlines():
                word = line.split()[0]
                words[word] = country

        new_df = pd.DataFrame(data=words.items(), columns=["word", "language"]).astype(
            "string"
        )
        language_df = pd.concat([language_df, new_df], ignore_index=True)

    memory.end()

    memory.start("Cleaning + vcr")
    language_df["word"] = language_df["word"].apply(remove_filler)
    language_df = language_df.dropna()
    language_df["ratio"] = language_df["word"].apply(calculate_vcr)
    memory.end()

    memory.start("Aggregation")
    for lang in countries:
        specific_df = language_df[(language_df["language"] == lang)]
        mean_ratio = specific_df["ratio"].sum()
        mean_ratio /= len(specific_df)
        vcr_dic[lang] = mean_ratio
        temperature_dic[lang] = float(country_avg_temperature_df[lang])
    memory.end()

    computation_tracker.end()
    memory.display_results()
    print("-" * 70)
    computation_tracker.display_results()
    scatter(temperature_dic, vcr_dic, countries)

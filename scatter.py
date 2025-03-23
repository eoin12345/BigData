import matplotlib.pyplot as plt
from lists_of_chars import colour_map, groups
from matplotlib.lines import Line2D
import pandas as pd


def scatter(temp_dic, ratio_dic, countries):
    plt.xlim(
        min(temp_dic.values()) - 0.2,
        max(temp_dic.values()) + 0.2,
    )
    plt.ylim(
        min(ratio_dic.values()) - 0.05,
        max(ratio_dic.values()) + 0.05,
    )

    df = pd.DataFrame(
        data={
            "country": countries,
            "vcr": [ratio_dic[country] for country in countries],
            "temperature": [temp_dic[country] for country in countries],
        }
    )
    corr = df["vcr"].corr(df["temperature"])

    ax = plt.gca()

    for country in countries:
        group = groups[country]
        colour = colour_map[group]
        ax.scatter(
            temp_dic[country], ratio_dic[country], label=country, color=colour, s=20
        )

    legend_languages = ax.legend(
        title="Languages", loc="upper left", bbox_to_anchor=(1, 1), fontsize=8
    )
    ax.add_artist(legend_languages)

    unique_groups = list(set(groups.values()))
    unique_groups = sorted(unique_groups)

    group_legend_elements = [
        Line2D(
            [0],
            [0],
            marker="o",
            color="w",
            label=group,
            markerfacecolor=colour_map[group],
            markersize=15,
        )
        for group in unique_groups
    ]

    legend_groups = ax.legend(
        handles=group_legend_elements,
        title="Groups",
        loc="lower right",
        bbox_to_anchor=(1, 0),
    )

    plt.ylabel("Ratio")
    plt.xlabel("Temperature")
    plt.suptitle("Vowel-Consonant-Ratio vs Temperature of Origin Country", fontsize=16)
    plt.title(f"Correlation: {corr}", fontsize=12)
    plt.show()
    df.to_csv("language_data.csv", index=False)

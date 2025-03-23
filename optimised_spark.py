import findspark
from scatter import scatter
from ratio import calculate_vcr_for_pair, remove_filler_for_pair
from lists_of_chars import frequencies
from never_optimised import countries, make_temperature_df, make_big_countries
from benchmarker import MemoryTracker

memory = MemoryTracker("Optimised spark")

if __name__ == "__main__":

    memory.start("Big countries")
    language_df = make_big_countries()
    memory.end()

    memory.start("Temperature")
    country_avg_temperature_df = make_temperature_df()
    memory.end()
    # set up spark

    memory.start("Setup spark")
    findspark.init()
    from pyspark.sql import SparkSession

    spark = (
        SparkSession.builder.master("local[16]")
        .config("spark.executor.memory", "6g")
        .config("spark.driver.memory", "8g")
        .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer")
        .config("spark.kryo.registrationRequired", "false")
        .config("spark.sql.shuffle.partitions", 48)
        .config("spark.default.parallelism", 48)
        .config("spark.sql.repl.eagerEval.enabled", True)
        .getOrCreate()
    )

    sc = spark.sparkContext
    # convert big countries data to spark rdd
    rdd = sc.parallelize(language_df.values.tolist())
    memory.end()

    memory.start("Spark computations")

    # Small countries
    def process_file(country_tuple):
        country, short = country_tuple
        file_path = f"../FrequencyWords/content/2018/{short}/{short}_full.txt"

        lines_rdd = sc.textFile(file_path)
        words_rdd = lines_rdd.map(lambda line: (line.split()[0], country))
        return words_rdd

    rdd_list = [process_file(item) for item in frequencies.items()]
    all_words_rdd = sc.union(rdd_list)

    rdd = sc.union([rdd, all_words_rdd])

    # print("number before cleaning",len(rdd.collect()))

    # clean data and get ratio
    rdd = rdd.map(remove_filler_for_pair)
    rdd = rdd.filter(lambda x: x[1] is not None and x[0] is not None)
    rdd = rdd.map(calculate_vcr_for_pair)

    # print("number after cleaning", len(rdd.collect()))

    rdd = (
        rdd.mapValues(lambda v: (v, 1))
        .reduceByKey(lambda a, b: (a[0] + b[0], a[1] + b[1]))
        .mapValues(lambda x: x[0] / x[1])
    )
    language_data = rdd.collect()
    memory.end()

    memory.display_results()

    temperature_dic = {}
    vcr_dic = {}

    for a, b in language_data:
        vcr_dic[a] = b
        temperature_dic[a] = float(country_avg_temperature_df[a])

    scatter(temperature_dic, vcr_dic, countries)

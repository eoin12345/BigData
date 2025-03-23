frequencies = {
    "Albania": "sq",
    "Bulgaria": "bg",
    "Denmark": "da",
    "Greece": "el",
    "Croatia": "hr",
    "Iceland": "is",
    "Latvia": "lv",
    "Macedonia": "mk",
    "The Netherlands": "nl",
    "Norway": "no",
    "Portugal": "pt",
    "Sweden": "sv",
    "Ukraine": "uk",
    "Romania": "ro",
}


vowels = {"a", "e", "i", "o", "u", "ą", "ę", "ó", "y", "ä", "ö", "ü"}  # Polish and German and general latin vowels


hungarian_vowels = {"a", "e", "i", "o", "ö", "u", "ü", "á", "é", "í", "ó", "ő", "ú", "ű"}
other_vowels = {"à", "á", "ã", "é", "è", "ê", "â", "î", "í", "ì", "ï", "ô", "õ", "ø", "ó", "ò", "û", "ü", "ú", "ù"}

albanian_special = {"ë"}
rus_vowels = {"а", "у", "о", "ы", "и", "э", "я", "ю", "ё", "е"}
rus_vowels_upper = set([x.upper() for x in rus_vowels])
greek_vowels = {"α", "ε", "η", "ι", "ο", "υ", "ω"}
greek_chars = {"έ", "ί", "ϊ", "ΐ", "ά", "ή", "ώ", "ό", "ύ", "ϋ", "ΰ"}

alleged_urdu_vowels = {"ا", "آ", "و", "ی", "ئ"}

catalan_vowels = {"a", "e", "i", "o", "u", "é", "è", "í", "ï", "ó", "ò", "ú", "ü"}
vowels = (
    vowels
    | rus_vowels
    | rus_vowels_upper
    | greek_vowels
    | hungarian_vowels
    | other_vowels
    | greek_chars
    | albanian_special
    | alleged_urdu_vowels
    | catalan_vowels
)


ignore = {"ь", "ъ", "´", "`", "ˆ", "˜", "¨", "¯", "˘", "¸", "˛", "ˇ", "˚", "˝", "˙", "ˤ", "ˀ", "ʰ", "ʲ", "ʷ", "ˠ", "ˬ",
          "ˮ"}
vowels = vowels | set([x.upper() for x in vowels])
ignore = ignore | set([x.upper() for x in ignore])


filler_chars = {".", ",", ";", ":", "!", "?", "-", "_", "=", "+", "(", ")", "[", "]", "{", "}", "<", ">", '"', "'", "/",
                "\\", "|", "&", "%", "$", "@", "#", "^", "~", "`", "*", "\n", "\t", "\r", " ", "..."}


digits = set([str(x) for x in range(10)])
fillers = digits | filler_chars | ignore


groups = {
    "Iceland": "Germanic",
    "Russia": "Slavic",
    "The Netherlands": "Germanic",
    "Macedonia": "Slavic",
    "Latvia": "Baltic",
    "Sweden": "Germanic",
    "Romania": "Romance",
    "Portugal": "Romance",
    "Germany": "Germanic",
    "Poland": "Slavic",
    "Greece": "Hellenic",
    "United Kingdom": "Germanic",
    "Ukraine": "Slavic",
    "Spain": "Romance",
    "France": "Romance",
    "Italy": "Romance",
    "Denmark": "Germanic",
    "Norway": "Germanic",
    "Albania": "Albanian",
    "Croatia": "Slavic",
    "Bulgaria": "Slavic",
}
colour_map = {
    "Germanic": "#1f77b4",
    "Slavic": "#d62728",
    "Romance": "#ff7f0e",
    "Baltic": "#2ca02c",
    "Hellenic": "#9467bd",
    "Albanian": "#8c564b",
}

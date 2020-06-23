#! python3
# english_monarch_name_translations.py - Produces csv with
#    names of English monarchs in different languages

# Import libraries
import requests
from bs4 import BeautifulSoup
import os
import pandas as pd

# Create a BeautifulSoup object from Wikipedia's "List of
#    English Monarchs"
url = "https://en.wikipedia.org/wiki/List_of_English_monarchs"
res = requests.get(url)
data = res.text
soup = BeautifulSoup(data, "lxml")

# Create a BeautifulSoup result set from the first columns
#    of each table
first_columns = soup.select("table tr td:nth-of-type(1)")

# Create a list to which to add the dictionaries
dicts = []

# Create a list to which to add hrefs to check for
#    duplicates
hrefs = []

# Get all <a> tags from first_columns
# Add the links and titles to a dictionary
for row in first_columns:
    tags = row.find_all("a")
    for tag in tags:
        # Check if href has already been added
        if tag.get("href") not in hrefs:
            # If it hasn't, add it to hrefs
            href = tag.get("href")
            hrefs.append(href)
            # Get page titles
            title = tag.get('title')
            if title is not None:
                # Remove en dashes and following text from
                #    titles. For instance, if the title is
                #    "Alfred le Grand – French", change it
                #    to "Alfred le Grand"
                en_dash = title.find("–")
                if en_dash > 0:
                    title = title[:en_dash-1]
                # Remove parenthetical text from titles.
                #    For instance, if the title is "Henri
                #    Ier (roi d'Angleterre", change it to
                #    "Henri Ier"
                paren = title.find("(")
                if paren > 0:
                    title = title[:paren-1]
                # Remove commas and following text from
                #    titles. For instance, if the title is
                #    "Vilim I, kralj Engleske", change it
                #    to "Vilim I"
                comma = title.find(",")
                if comma > 0:
                    title = title[:comma]
            if href is not None:
                # Remove hrefs for notes
                if href.startswith("/wiki/"):
                    # Remove hrefs for files
                    if href.startswith("/wiki/File"):
                        continue
                    else:
                        # Create a dictionary out of the
                        #    tag
                        href = {
                            "URL": str("https://en.wikipedia.org" + href),
                            "English": title
                            }
                    # Add the newly-created dictionary to
                    #    dicts
                    dicts.append(href)
        else:
            continue

# Create dictionary of Wikipedia language codes, taken
#    from https://en.wikipedia.org/wiki/List_of_Wikipedias
language_tags = {
    "en": "English",
    "fr": "French",
    "de": "German",
    "es": "Spanish",
    "ja": "Japanese",
    "ru": "Russian",
    "it": "Italian",
    "zh": "Chinese",
    "pt": "Portuguese",
    "ar": "Arabic",
    "fa": "Persian",
    "pl": "Polish",
    "nl": "Dutch",
    "id": "Indonesian",
    "uk": "Ukrainian",
    "he": "Hebrew",
    "sv": "Swedish",
    "cs": "Czech",
    "ko": "Korean",
    "vi": "Vietnamese",
    "ca": "Catalan",
    "no": "Norwegian (Bokmål)",
    "fi": "Finnish",
    "hu": "Hungarian",
    "tr": "Turkish",
    "sr": "Serbian",
    "el": "Greek",
    "th": "Thai",
    "hi": "Hindi",
    "bn": "Bengali",
    "simple": "Simple English",
    "ceb": "Cebuano",
    "ro": "Romanian",
    "sw": "Swahili",
    "kk": "Kazakh",
    "da": "Danish",
    "eo": "Esperanto",
    "lt": "Lithuanian",
    "sk": "Slovak",
    "bg": "Bulgarian",
    "sl": "Slovene",
    "eu": "Basque",
    "et": "Estonian",
    "hr": "Croatian",
    "ms": "Malay",
    "arz": "Egyptian Arabic",
    "ur": "Urdu",
    "ta": "Tamil",
    "te": "Telugu language",
    "nn": "Norwegian (Nynorsk)",
    "gl": "Galician",
    "az": "Azerbaijani",
    "af": "Afrikaans",
    "bs": "Bosnian",
    "be": "Belarusian",
    "ml": "Malayalam",
    "ka": "Georgian",
    "is": "Icelandic",
    "sq": "Albanian",
    "la": "Latin",
    "mk": "Macedonian",
    "lv": "Latvian",
    "azb": "Southern Azerbaijani",
    "mr": "Marathi",
    "sh": "Serbo-Croatian",
    "tl": "Tagalog",
    "cy": "Welsh",
    "ku": "Kurdish (Kurmanji)",
    "ckb": "Sorani Kurdish",
    "ast": "Asturian",
    "oc": "Occitan",
    "jv": "Javanese",
    "be-tarask": "Belarusian (Taraškievica)",
    "zh-yue": "Cantonese",
    "ga": "Irish",
    "hy": "Armenian",
    "pa": "Eastern Punjabi",
    "as": "Assamese",
    "my": "Burmese",
    "kn": "Kannada language",
    "ne": "Nepali",
    "sco": "Scots",
    "si": "Sinhalese",
    "tt": "Tatar",
    "uz": "Uzbek",
    "war": "Waray",
    "vo": "Volapük",
    "min": "Minangkabau",
    "lmo": "Lombard",
    "new": "Newar / Nepal Bhasa",
    "ht": "Haitian",
    "lb": "Luxembourgish",
    "br": "Breton",
    "gu": "Gujarati",
    "tg": "Tajik",
    "bpy": "Bishnupriya Manipuri",
    "io": "Ido",
    "pms": "Piedmontese",
    "su": "Sundanese",
    "nap": "Neapolitan",
    "zh-min-nan": "Min Nan",
    "nds": "Low Saxon",
    "ba": "Bashkir",
    "scn": "Sicilian",
    "wa": "Walloon",
    "bar": "Bavarian",
    "an": "Aragonese",
    "ksh": "Ripuarian",
    "szl": "Silesian",
    "fy": "West Frisian",
    "frr": "North Frisian",
    "als": "Alemannic",
    "ia": "Interlingua",
    "yi": "Yiddish",
    "mg": "Malagasy",
    "gd": "Scottish Gaelic",
    "vec": "Venetian",
    "ce": "Chechen",
    "sa": "Sanskrit",
    "mai": "Maithili",
    "xmf": "Mingrelian",
    "sd": "Sindhi",
    "wuu": "Wu",
    "km": "Khmer",
    "roa-tara": "Tarantino",
    "am": "Amharic",
    "roa-rup": "Aromanian",
    "map-bms": "Banyumasan",
    "bh": "Bhojpuri",
    "bcl": "Central_Bicolano",
    "co": "Corsican",
    "cv": "Chuvash",
    "dv": "Divehi",
    "nds-nl": "Dutch Low Saxon",
    "fo": "Faroese",
    "fur": "Friulian",
    "gan": "Gan Chinese",
    "glk": "Gilaki",
    "gu": "Gujarati",
    "ilo": "Ilokano",
    "pam": "Kapampangan",
    "csb": "Kashubian",
    "lij": "Ligurian",
    "li": "Limburgish",
    "gv": "Manx",
    "mi": "Māori",
    "mt": "Maltese",
    "nah": "Nāhuatl",
    "nrm": "Norman",
    "se": "Northern Sami",
    "nov": "Novial",
    "qu": "Quechua",
    "os": "Ossetian",
    "pi": "Pali",
    "pag": "Pangasinan",
    "ps": "Pashto",
    "pdc": "Pennsylvania German",
    "rm": "Romansh",
    "bat-smg": "Samogitian",
    "sc": "Sardinian",
    "to": "Tongan",
    "tk": "Turkmen",
    "hsb": "Upper Sorbian",
    "fiu-vro": "Võro",
    "vls": "West Flemish",
    "yo": "Yoruba",
    "diq": "Zazaki",
    "zh-classical": "Classical Chinese",
    "frp": "Franco-Provençal/Arpitan",
    "lad": "Ladino",
    "kw": "Cornish",
    "mn": "Mongolian",
    "haw": "Hawaiian",
    "ang": "Anglo-Saxon",
    "ln": "Lingala",
    "ie": "Interlingue",
    "wo": "Wolof",
    "tpi": "Tok Pisin",
    "ty": "Tahitian",
    "crh": "Crimean Tatar",
    "nv": "Navajo",
    "jbo": "Lojban",
    "ay": "Aymara",
    "pcd": "Picard",
    "zea": "Zealandic",
    "eml": "Emilian-Romagnol",
    "ky": "Kyrgyz",
    "ig": "Igbo",
    "or": "Odia",
    "cbk-zam": "Zamboanga Chavacano",
    "kg": "Kongo",
    "arc": "Syriac",
    "rmy": "Vlax Romani",
    "ab": "Abkhazian",
    "gn": "Guarani",
    "so": "Somali",
    "kab": "Kabyle",
    "ug": "Uyghur",
    "stq": "Saterland Frisian",
    "ha": "Hausa",
    "udm": "Udmurt",
    "ext": "Extremaduran",
    "mzn": "Mazandarani",
    "pap": "Papiamentu",
    "cu": "Old Church Slavonic",
    "sah": "Sakha",
    "tet": "Tetum",
    "sn": "Shona",
    "lo": "Lao",
    "pnb": "Western Punjabi",
    "iu": "Inuktitut",
    "na": "Nauruan",
    "got": "Gothic",
    "bo": "Tibetan",
    "dsb": "Lower Sorbian",
    "chr": "Cherokee",
    "cdo": "Min Dong",
    "hak": "Hakka",
    "om": "Oromo",
    "sm": "Samoan",
    "ee": "Ewe",
    "ti": "Tigrinya",
    "av": "Avar",
    "bm": "Bambara",
    "zu": "Zulu",
    "pnt": "Pontic",
    "cr": "Cree",
    "pih": "Norfolk",
    "ss": "Swati",
    "ve": "Venda",
    "bi": "Bislama",
    "rw": "Kinyarwanda",
    "ch": "Chamorro",
    "xh": "Xhosa",
    "kl": "Greenlandic",
    "ik": "Inupiak",
    "bug": "Buginese",
    "dz": "Dzongkha",
    "ts": "Tsonga",
    "tn": "Tswana",
    "kv": "Komi",
    "tum": "Tumbuka",
    "xal": "Kalmyk",
    "st": "Sesotho",
    "tw": "Twi",
    "bxr": "Buryat (Russia)",
    "ak": "Akan",
    "ny": "Chichewa",
    "fj": "Fijian",
    "lbe": "Lak",
    "ki": "Kikuyu",
    "za": "Zhuang",
    "ks": "Kashmiri",
    "ff": "Fula",
    "lg": "Luganda",
    "sg": "Sango",
    "rn": "Kirundi",
    "chy": "Cheyenne",
    "mwl": "Mirandese",
    "lez": "Lezgian",
    "bjn": "Banjar",
    "gom": "Konkani",
    "lrc": "Northern Luri",
    "tyv": "Tuvan",
    "vep": "Veps",
    "nso": "Northern Sotho",
    "kbd": "Kabardian",
    "ltg": "Latgalian",
    "rue": "Rusyn",
    "pfl": "Palatine German",
    "gag": "Gagauz",
    "koi": "Komi-Permyak",
    "mrj": "Hill Mari",
    "mhr": "Meadow Mari",
    "krc": "Karachay-Balkar",
    "ace": "Acehnese",
    "hif": "Fiji Hindi",
    "olo": "Livvi-Karelian",
    "kaa": "Karakalpak",
    "mdf": "Moksha",
    "myv": "Erzya",
    "srn": "Sranan Tongo",
    "ady": "Adyghe",
    "jam": "Jamaican",
    "tcy": "Tulu",
    "dty": "Doteli",
    "kbp": "Kabiye",
    "din": "Dinka",
    "lfn": "Lingua Franca Nova",
    "gor": "Gorontalo",
    "inh": "Ingush",
    "sat": "Santali",
    "shn": "Shan",
    "hyw": "Western Armenian",
    "nqo": "N'Ko",
    "ban": "Balinese",
    "mnw": "Mon",
    "szy": "Sakizaya",
    "gcr": "Guianan Creole",
    "awa": "Awadhi",
    "atj": "Atikamekw"
    }

for dict in dicts:
    # Create a BeautifulSoup object for each URL added
    #    above
    url = dict["URL"]
    res = requests.get(url)
    data = res.text
    soup = BeautifulSoup(data, "lxml")
    # Find all <a> tags with the class
    #    "interlanguage-link-target"
    tags = soup.find_all("a",
                         {"class":
                          "interlanguage-link-target"})
    for tag in tags:
        # Get page title
        title = tag["title"]
        if title is not None:
            # Remove en dashes and following text from
            #    titles. For instance, if the title is
            #    "Alfred le Grand – French", change it
            #    to "Alfred le Grand"
            en_dash = title.find("–")
            if en_dash > 0:
                title = title[:en_dash-1]
            # Remove parenthetical text from titles.
            #    For instance, if the title is "Henri
            #    Ier (roi d'Angleterre", change it to
            #    "Henri Ier"
            paren = title.find("(")
            if paren > 0:
                title = title[:paren-1]
            # Remove commas and following text from
            #    titles. For instance, if the title is
            #    "Vilim I, kralj Engleske", change it
            #    to "Vilim I"
            comma = title.find(",")
            if comma > 0:
                title = title[:comma]
                # print(tag["lang"]) # test
        try:
            # Add the title to the dictionary
            dict[language_tags[tag["lang"]]] = title
        except:
            continue

# Change to the directory in which to save the csv
os.chdir("C:/Users/username/Documents")
# Create a dataframe out of dicts
df = pd.DataFrame(dicts)
# Write the dataframe to csv
df.to_csv("english_monarchs.csv", encoding="utf-8-sig")

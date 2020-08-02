#! python3
# english_monarch_name_translations.py

"""
This program produces a csv with the names of English monarchs in
    different languages.
"""

# Import libraries
import requests
from bs4 import BeautifulSoup
import os
import pandas as pd

# Scrape Wikipedia's "List of English Monarchs".
url = "https://en.wikipedia.org/wiki/List_of_English_monarchs"
res = requests.get(url)
data = res.text
soup = BeautifulSoup(data, "lxml")

# Create a BeautifulSoup result set from the first columns of the page's
#   tables.
first_columns = soup.select("table tr td:nth-of-type(1)")

# Create lists to which to add dictionaries for the monarchs. One list
#   will include only the English language pages. The other will include
#   entries for all languages.
english_dicts = []
all_dicts = []

# Create a list to which to add hrefs to check for duplicates. (Hrefs
#   will serve as unique identifiers for the monarchs.)
hrefs = []

# Get all <a> tags from first_columns. For each <a> tag, add the link
#   and title to a dictionary for the monarch.
for row in first_columns:
    tags = row.find_all("a")
    for tag in tags:
        href = tag.get("href")
        if href not in hrefs:
            if href is not None:
                if href.startswith("/wiki/"):
                    if not href.startswith("/wiki/File"):
                        hrefs.append(href)
                        title = tag.get("title")
                        if title is not None:
                            # Remove en dashes and following text from
                            #   titles. For instance, if the title is
                            #   "Alfred le Grand - French", change it to
                            #   "Alfred le Grand".
                            en_dash = title.find("–")
                            if en_dash > 0:
                                title = title[:en_dash-1]
                            # Remove parenthetical text from titles. For
                            #   instance, if the title is "Henry Ier
                            #   (roi d'Angleterre)", change it to "Henri
                            #   Ier".
                            paren = title.find("(")
                            if paren > 0:
                                title = title[:paren-1]
                            # Remove commas and following text from
                            #   titles. For instance, if the title is
                            #   "Vilim I, kralj Engleske", change it to
                            #   "Vilim I".
                            comma = title.find(",")
                            if comma > 0:
                                title = title[:comma]
                            # Get the first word of the title.
                            space = title.find(" ")
                            if space > 0:
                                title_first_word = title[:space]
                            else:
                                title_first_word = title
                            # Create a dictionary for the monarch.
                            href = {
                                "Name (English)": title_first_word,
                                "Full Name (English)": title,
                                "URL": "https://en.wikipedia.org" +
                                    href,
                                "Language": "English",
                                "Name": title_first_word,
                                "Full Name": title,
                                "Familiar-ish Script": "Yes",
                                "Given Name Usually First": "Yes"
                                }
                            # Add the newly-created dictionary to the
                            #   lists.
                            english_dicts.append(href)
                            all_dicts.append(href)

# Create a dictionary of Wikipedia languages. Language codes and names
#   are taken from https://en.wikipedia.org/wiki/List_of_Wikipedias. For
#   each language, I have also noted whether the language is written in
#   a script that I can at least partially make sense of ("fs" for
#   "familiar script"), and if so, whether, in that language, a person's
#   given name tends to appear before their surname ("gnf" for "given
#   name first") in the title of their Wikipedia entry.
language_tags = {
    "ab": {"name": "Abkhazian", "fs": "Yes", "gnf": "Yes"},
    "ace": {"name": "Acehnese", "fs": "Yes", "gnf": "Yes"},
    "ady": {"name": "Adyghe", "fs": "Yes", "gnf": "Yes"},
    "af": {"name": "Afrikaans", "fs": "Yes", "gnf": "Yes"},
    "ak": {"name": "Akan", "fs": "Yes", "gnf": "Yes"},
    # "als" may not remain the code for Alemannic, as it is the ISO
    #   639-3 code for Tosk Albanian. "gsw" is in consideration as an
    #   alternative.
    "als": {"name": "Alemannic", "fs": "Yes", "gnf": "Yes"},
    "am": {"name": "Amharic", "fs": "No", "gnf": "idk"},
    "an": {"name": "Aragonese", "fs": "Yes", "gnf": "Yes"},
    "ang": {"name": "Anglo-Saxon", "fs": "Yes", "gnf": "Yes"},
    "ar": {"name": "Arabic", "fs": "Yes", "gnf": "Yes"},
    "arc": {"name": "Syriac", "fs": "No", "gnf": "idk"},
    "arz": {"name": "Egyptian Arabic", "fs": "Yes", "gnf": "Yes"},
    "as": {"name": "Assamese", "fs": "No", "gnf": "idk"},
    "ast": {"name": "Asturian", "fs": "Yes", "gnf": "Yes"},
    "atj": {"name": "Atikamekw", "fs": "Yes", "gnf": "Yes"},
    "av": {"name": "Avar", "fs": "Yes", "gnf": "Yes"},
    "awa": {"name": "Awadhi", "fs": "No", "gnf": "idk"},
    "ay": {"name": "Aymara", "fs": "Yes", "gnf": "Yes"},
    "az": {"name": "Azerbaijani", "fs": "Yes", "gnf": "No"},
    "azb": {"name": "Southern Azerbaijani", "fs": "Yes", "gnf": "No"},
    "ba": {"name": "Bashkir", "fs": "Yes", "gnf": "No"},
    "ban": {"name": "Balinese", "fs": "Yes", "gnf": "Yes"},
    "bar": {"name": "Bavarian", "fs": "Yes", "gnf": "Yes"},
    # "bat-smg" is a nonstandard variant of "sgs".
    "bat-smg": {"name": "Samogitian", "fs": "Yes", "gnf": "Yes"},
    "bcl": {"name": "Central_Bicolano", "fs": "Yes", "gnf": "No"},
    "be": {"name": "Belarusian", "fs": "Yes", "gnf": "Yes"},
    "be-tarask": {
        "name": "Belarusian (Taraškievica)", "fs": "Yes", "gnf": "Yes"},
    # "be-x-old" is a nonstandard variant of "be-tarask".
    "be-x-old": {
        "name": "Belarusian (Taraškievica)", "fs": "Yes", "gnf": "Yes"},
    "bg": {"name": "Bulgarian", "fs": "Yes", "gnf": "Yes"},
    "bh": {"name": "Bhojpuri", "fs": "No", "gnf": "idk"},
    "bi": {"name": "Bislama", "fs": "Yes", "gnf": "Yes"},
    "bjn": {"name": "Banjar", "fs": "Yes", "gnf": "Yes"},
    "bm": {"name": "Bambara", "fs": "Yes", "gnf": "Yes"},
    "bn": {"name": "Bengali", "fs": "No", "gnf": "idk"},
    "bo": {"name": "Tibetan", "fs": "No", "gnf": "idk"},
    "bpy": {"name": "Bishnupriya Manipuri", "fs": "No", "gnf": "idk"},
    "br": {"name": "Breton", "fs": "Yes", "gnf": "Yes"},
    "bs": {"name": "Bosnian", "fs": "Yes", "gnf": "Yes"},
    "bug": {"name": "Buginese", "fs": "Yes", "gnf": "Yes"},
    "bxr": {"name": "Buryat (Russia)", "fs": "Yes", "gnf": "No"},
    "ca": {"name": "Catalan", "fs": "Yes", "gnf": "Yes"},
    # cbk is a nonstandardized code.
    "cbk": {"name": "Zamboanga Chavacano", "fs": "Yes", "gnf": "Yes"},
    # "cbk-zam" is a nonstandardized code.
    "cbk-zam": {"name": "Zamboanga Chavacano", "fs": "Yes", "gnf": "Yes"},
    "cdo": {"name": "Min Dong", "fs": "Yes", "gnf": "Yes"},
    "ce": {"name": "Chechen", "fs": "Yes", "gnf": "Yes"},
    "ceb": {"name": "Cebuano", "fs": "Yes", "gnf": "Yes"},
    "ch": {"name": "Chamorro", "fs": "Yes", "gnf": "Yes"},
    "chr": {"name": "Cherokee", "fs": "No", "gnf": "idk"},
    "chy": {"name": "Cheyenne", "fs": "Yes", "gnf": "Yes"},
    "ckb": {"name": "Sorani Kurdish", "fs": "Yes", "gnf": "Yes"},
    "co": {"name": "Corsican", "fs": "Yes", "gnf": "Yes"},
    "cr": {"name": "Cree", "fs": "Yes", "gnf": "Yes"},
    "crh": {"name": "Crimean Tatar", "fs": "Yes", "gnf": "No"},
    "cs": {"name": "Czech", "fs": "Yes", "gnf": "Yes"},
    "csb": {"name": "Kashubian", "fs": "Yes", "gnf": "Yes"},
    "cu": {"name": "Old Church Slavonic", "fs": "Yes", "gnf": "Yes"},
    "cv": {"name": "Chuvash", "fs": "Yes", "gnf": "Yes"},
    "cy": {"name": "Welsh", "fs": "Yes", "gnf": "Yes"},
    # "cz" is a nonstandard variant of "cs".
    "cz": {"name": "Czech", "fs": "Yes", "gnf": "Yes"},
    "da": {"name": "Danish", "fs": "Yes", "gnf": "Yes"},
    "de": {"name": "German", "fs": "Yes", "gnf": "Yes"},
    "din": {"name": "Dinka", "fs": "Yes", "gnf": "Yes"},
    "diq": {"name": "Zazaki", "fs": "Yes", "gnf": "Yes"},
    # "dk" is a nonstandard variant of "da".
    "dk": {"name": "Danish", "fs": "Yes", "gnf": "Yes"},
    "dsb": {"name": "Lower Sorbian", "fs": "Yes", "gnf": "Yes"},
    "dty": {"name": "Doteli", "fs": "No", "gnf": "idk"},
    "dv": {"name": "Divehi", "fs": "No", "gnf": "idk"},
    "dz": {"name": "Dzongkha", "fs": "No", "gnf": "idk"},
    "ee": {"name": "Ewe", "fs": "Yes", "gnf": "Yes"},
    "el": {"name": "Greek", "fs": "Yes", "gnf": "Yes"},
    "eml": {"name": "Emilian-Romagnol", "fs": "Yes", "gnf": "Yes"},
    "en": {"name": "English", "fs": "Yes", "gnf": "Yes"},
    "en-simple": {"name": "Simple English", "fs": "Yes", "gnf": "Yes"},
    "eo": {"name": "Esperanto", "fs": "Yes", "gnf": "Yes"},
    "es": {"name": "Spanish", "fs": "Yes", "gnf": "Yes"},
    "et": {"name": "Estonian", "fs": "Yes", "gnf": "Yes"},
    "eu": {"name": "Basque", "fs": "Yes", "gnf": "Yes"},
    "ext": {"name": "Extremaduran", "fs": "Yes", "gnf": "Yes"},
    "fa": {"name": "Persian", "fs": "Yes", "gnf": "Yes"},
    "ff": {"name": "Fula", "fs": "Yes", "gnf": "Yes"},
    "fi": {"name": "Finnish", "fs": "Yes", "gnf": "Yes"},
    # "fiu" is a nonstandard variant of "vro".
    "fiu": {"name": "Võro", "fs": "Yes", "gnf": "Yes"},
    # "fiu-vro" is a nonstandard variant of "vro".
    "fiu-vro": {"name": "Võro", "fs": "Yes", "gnf": "Yes"},
    "fj": {"name": "Fijian", "fs": "Yes", "gnf": "Yes"},
    "fo": {"name": "Faroese", "fs": "Yes", "gnf": "Yes"},
    "fr": {"name": "French", "fs": "Yes", "gnf": "Yes"},
    "frp": {"name": "Franco-Provençal/Arpitan", "fs": "Yes", "gnf": "Yes"},
    "frr": {"name": "North Frisian", "fs": "Yes", "gnf": "Yes"},
    "fur": {"name": "Friulian", "fs": "Yes", "gnf": "No"},
    "fy": {"name": "West Frisian", "fs": "Yes", "gnf": "Yes"},
    "ga": {"name": "Irish", "fs": "Yes", "gnf": "Yes"},
    "gag": {"name": "Gagauz", "fs": "Yes", "gnf": "Yes"},
    "gan": {"name": "Gan Chinese", "fs": "No", "gnf": "idk"},
    "gcr": {"name": "Guianan Creole", "fs": "Yes", "gnf": "Yes"},
    "gd": {"name": "Scottish Gaelic", "fs": "Yes", "gnf": "Yes"},
    "gl": {"name": "Galician", "fs": "Yes", "gnf": "Yes"},
    "glk": {"name": "Gilaki", "fs": "Yes", "gnf": "Yes"},
    "gn": {"name": "Guarani", "fs": "Yes", "gnf": "Yes"},
    "gom": {"name": "Konkani", "fs": "Yes", "gnf": "No"},
    "gor": {"name": "Gorontalo", "fs": "Yes", "gnf": "Yes"},
    "got": {"name": "Gothic", "fs": "No", "gnf": "idk"},
    # "gsw" is not the official code for Alemannic, but it is in
    #   consideration to replace the currently used "als", since "als"
    #   is the ISO 639-3 code for Tosk Albanian.
    "gsw": {"name": "Alemannic", "fs": "Yes", "gnf": "Yes"},
    "gu": {"name": "Gujarati", "fs": "No", "gnf": "idk"},
    "gu": {"name": "Gujarati", "fs": "No", "gnf": "idk"},
    "gv": {"name": "Manx", "fs": "Yes", "gnf": "Yes"},
    "ha": {"name": "Hausa", "fs": "Yes", "gnf": "Yes"},
    "hak": {"name": "Hakka", "fs": "Yes", "gnf": "Yes"},
    "haw": {"name": "Hawaiian", "fs": "Yes", "gnf": "Yes"},
    "he": {"name": "Hebrew", "fs": "No", "gnf": "idk"},
    "hi": {"name": "Hindi", "fs": "No", "gnf": "idk"},
    "hif": {"name": "Fiji Hindi", "fs": "Yes", "gnf": "Yes"},
    "hr": {"name": "Croatian", "fs": "Yes", "gnf": "Yes"},
    "hsb": {"name": "Upper Sorbian", "fs": "Yes", "gnf": "Yes"},
    "ht": {"name": "Haitian", "fs": "Yes", "gnf": "Yes"},
    "hu": {"name": "Hungarian", "fs": "Yes", "gnf": "No"},
    "hy": {"name": "Armenian", "fs": "No", "gnf": "idk"},
    "hyw": {"name": "Western Armenian", "fs": "No", "gnf": "idk"},
    "ia": {"name": "Interlingua", "fs": "Yes", "gnf": "Yes"},
    "id": {"name": "Indonesian", "fs": "Yes", "gnf": "Yes"},
    "ie": {"name": "Interlingue", "fs": "Yes", "gnf": "Yes"},
    "ig": {"name": "Igbo", "fs": "Yes", "gnf": "Yes"},
    "ik": {"name": "Inupiak", "fs": "Yes", "gnf": "Yes"},
    "ilo": {"name": "Ilokano", "fs": "Yes", "gnf": "Yes"},
    "inh": {"name": "Ingush", "fs": "Yes", "gnf": "No"},
    "io": {"name": "Ido", "fs": "Yes", "gnf": "Yes"},
    "is": {"name": "Icelandic", "fs": "Yes", "gnf": "Yes"},
    "it": {"name": "Italian", "fs": "Yes", "gnf": "Yes"},
    "iu": {"name": "Inuktitut", "fs": "No", "gnf": "idk"},
    "ja": {"name": "Japanese", "fs": "No", "gnf": "idk"},
    "jam": {"name": "Jamaican", "fs": "Yes", "gnf": "Yes"},
    "jbo": {"name": "Lojban", "fs": "Yes", "gnf": "No"},
    "jv": {"name": "Javanese", "fs": "Yes", "gnf": "Yes"},
    "ka": {"name": "Georgian", "fs": "No", "gnf": "idk"},
    "kaa": {"name": "Karakalpak", "fs": "Yes", "gnf": "Yes"},
    "kab": {"name": "Kabyle", "fs": "Yes", "gnf": "Yes"},
    "kbd": {"name": "Kabardian", "fs": "Yes", "gnf": "Yes"},
    "kbp": {"name": "Kabiye", "fs": "Yes", "gnf": "Yes"},
    "kg": {"name": "Kongo", "fs": "Yes", "gnf": "Yes"},
    "ki": {"name": "Kikuyu", "fs": "Yes", "gnf": "Yes"},
    "kk": {"name": "Kazakh", "fs": "Yes", "gnf": "No"},
    "kl": {"name": "Greenlandic", "fs": "Yes", "gnf": "Yes"},
    "km": {"name": "Khmer", "fs": "No", "gnf": "idk"},
    "kn": {"name": "Kannada language", "fs": "No", "gnf": "idk"},
    "ko": {"name": "Korean", "fs": "No", "gnf": "idk"},
    "koi": {"name": "Komi-Permyak", "fs": "Yes", "gnf": "No"},
    "krc": {"name": "Karachay-Balkar", "fs": "Yes", "gnf": "Yes"},
    "ks": {"name": "Kashmiri", "fs": "No", "gnf": "idk"},
    # There may be some issue with the code "ksh".
    "ksh": {"name": "Ripuarian", "fs": "Yes", "gnf": "Yes"},
    "ku": {"name": "Kurdish (Kurmanji)", "fs": "Yes", "gnf": "Yes"},
    "kv": {"name": "Komi", "fs": "Yes", "gnf": "No"},
    "kw": {"name": "Cornish", "fs": "Yes", "gnf": "Yes"},
    "ky": {"name": "Kyrgyz", "fs": "Yes", "gnf": "Yes"},
    "la": {"name": "Latin", "fs": "Yes", "gnf": "Yes"},
    "lad": {"name": "Ladino", "fs": "Yes", "gnf": "Yes"},
    "lb": {"name": "Luxembourgish", "fs": "Yes", "gnf": "Yes"},
    "lbe": {"name": "Lak", "fs": "Yes", "gnf": "Yes"},
    "lez": {"name": "Lezgian", "fs": "Yes", "gnf": "No"},
    "lfn": {"name": "Lingua Franca Nova", "fs": "Yes", "gnf": "Yes"},
    "lg": {"name": "Luganda", "fs": "Yes", "gnf": "Yes"},
    "li": {"name": "Limburgish", "fs": "Yes", "gnf": "Yes"},
    "lij": {"name": "Ligurian", "fs": "Yes", "gnf": "Yes"},
    "lmo": {"name": "Lombard", "fs": "Yes", "gnf": "Yes"},
    "ln": {"name": "Lingala", "fs": "Yes", "gnf": "Yes"},
    "lo": {"name": "Lao", "fs": "No", "gnf": "idk"},
    "lrc": {"name": "Northern Luri", "fs": "Yes", "gnf": "Yes"},
    "lt": {"name": "Lithuanian", "fs": "Yes", "gnf": "Yes"},
    "ltg": {"name": "Latgalian", "fs": "Yes", "gnf": "Yes"},
    "lv": {"name": "Latvian", "fs": "Yes", "gnf": "Yes"},
    "lzh": {"name": "Classical Chinese", "fs": "No", "gnf": "idk"},
    "mai": {"name": "Maithili", "fs": "No", "gnf": "idk"},
    # "map" is a nonstandardized code.
    "map": {"name": "Banyumasan", "fs": "Yes", "gnf": "Yes"},
    # "map-bms" is a nonstandardized code.
    "map-bms": {"name": "Banyumasan", "fs": "Yes", "gnf": "Yes"},
    "mdf": {"name": "Moksha", "fs": "Yes", "gnf": "No"},
    "mg": {"name": "Malagasy", "fs": "Yes", "gnf": "Yes"},
    "mhr": {"name": "Meadow Mari", "fs": "Yes", "gnf": "No"},
    "mi": {"name": "Māori", "fs": "Yes", "gnf": "Yes"},
    "min": {"name": "Minangkabau", "fs": "Yes", "gnf": "Yes"},
    "mk": {"name": "Macedonian", "fs": "Yes", "gnf": "Yes"},
    "ml": {"name": "Malayalam", "fs": "No", "gnf": "idk"},
    "mn": {"name": "Mongolian", "fs": "Yes", "gnf": "No"},
    "mnw": {"name": "Mon", "fs": "No", "gnf": "idk"},
    # "mo" is a nonstandard variant of "ro".
    "mo": {"name": "Romanian", "fs": "Yes", "gnf": "Yes"},
    "mr": {"name": "Marathi", "fs": "No", "gnf": "idk"},
    "mrj": {"name": "Hill Mari", "fs": "Yes", "gnf": "No"},
    "ms": {"name": "Malay", "fs": "Yes", "gnf": "Yes"},
    "mt": {"name": "Maltese", "fs": "Yes", "gnf": "Yes"},
    "mwl": {"name": "Mirandese", "fs": "Yes", "gnf": "Yes"},
    "my": {"name": "Burmese", "fs": "No", "gnf": "idk"},
    "myv": {"name": "Erzya", "fs": "Yes", "gnf": "No"},
    "mzn": {"name": "Mazandarani", "fs": "Yes", "gnf": "Yes"},
    "na": {"name": "Nauruan", "fs": "Yes", "gnf": "Yes"},
    "nah": {"name": "Nāhuatl", "fs": "Yes", "gnf": "No"},
    "nan": {"name": "Min Nan", "fs": "Yes", "gnf": "Yes"},
    "nap": {"name": "Neapolitan", "fs": "Yes", "gnf": "Yes"},
    # "nb" is a nonstandard variant of "no".
    "nb": {"name": "Norwegian (Bokmål)", "fs": "Yes", "gnf": "Yes"},
    # "nds" is sometimes incorrectly used to refer to Dutch Low Saxon
    #   ("nds-NL").
    "nds": {"name": "Low Saxon", "fs": "Yes", "gnf": "Yes"},
    # "nds-nl" and "nds-NL" refer to the same language.
    "nds-nl": {"name": "Dutch Low Saxon", "fs": "Yes", "gnf": "Yes"},
    "nds-NL": {"name": "Dutch Low Saxon", "fs": "Yes", "gnf": "Yes"},
    "ne": {"name": "Nepali", "fs": "No", "gnf": "idk"},
    "new": {"name": "Newar / Nepal Bhasa", "fs": "No", "gnf": "idk"},
    "nl": {"name": "Dutch", "fs": "Yes", "gnf": "Yes"},
    "nn": {"name": "Norwegian (Nynorsk)", "fs": "Yes", "gnf": "Yes"},
    "no": {"name": "Norwegian (Bokmål)", "fs": "Yes", "gnf": "Yes"},
    "nov": {"name": "Novial", "fs": "Yes", "gnf": "Yes"},
    "nqo": {"name": "N'Ko", "fs": "No", "gnf": "idk"},
    "nrf": {"name": "Norman", "fs": "Yes", "gnf": "Yes"},
    # "nrm" is a nonstandard variant of "nrf".
    "nrm": {"name": "Norman", "fs": "Yes", "gnf": "Yes"},
    "nso": {"name": "Northern Sotho", "fs": "Yes", "gnf": "Yes"},
    "nv": {"name": "Navajo", "fs": "Yes", "gnf": "No"},
    "ny": {"name": "Chichewa", "fs": "Yes", "gnf": "Yes"},
    "oc": {"name": "Occitan", "fs": "Yes", "gnf": "Yes"},
    "olo": {"name": "Livvi-Karelian", "fs": "Yes", "gnf": "Yes"},
    "om": {"name": "Oromo", "fs": "Yes", "gnf": "Yes"},
    "or": {"name": "Odia", "fs": "No", "gnf": "idk"},
    "os": {"name": "Ossetian", "fs": "Yes", "gnf": "Yes"},
    "pa": {"name": "Eastern Punjabi", "fs": "No", "gnf": "idk"},
    "pag": {"name": "Pangasinan", "fs": "Yes", "gnf": "Yes"},
    "pam": {"name": "Kapampangan", "fs": "Yes", "gnf": "Yes"},
    "pap": {"name": "Papiamentu", "fs": "Yes", "gnf": "Yes"},
    "pcd": {"name": "Picard", "fs": "Yes", "gnf": "No"},
    "pdc": {"name": "Pennsylvania German", "fs": "Yes", "gnf": "Yes"},
    "pfl": {"name": "Palatine German", "fs": "Yes", "gnf": "Yes"},
    "pi": {"name": "Pali", "fs": "No", "gnf": "idk"},
    "pih": {"name": "Norfolk", "fs": "Yes", "gnf": "Yes"},
    "pl": {"name": "Polish", "fs": "Yes", "gnf": "Yes"},
    "pms": {"name": "Piedmontese", "fs": "Yes", "gnf": "Yes"},
    "pnb": {"name": "Western Punjabi", "fs": "Yes", "gnf": "Yes"},
    "pnt": {"name": "Pontic", "fs": "Yes", "gnf": "Yes"},
    "ps": {"name": "Pashto", "fs": "Yes", "gnf": "No"},
    "pt": {"name": "Portuguese", "fs": "Yes", "gnf": "Yes"},
    "qu": {"name": "Quechua", "fs": "Yes", "gnf": "Yes"},
    "rm": {"name": "Romansh", "fs": "Yes", "gnf": "Yes"},
    "rmy": {"name": "Vlax Romani", "fs": "Yes", "gnf": "Yes"},
    "rn": {"name": "Kirundi", "fs": "Yes", "gnf": "Yes"},
    "ro": {"name": "Romanian", "fs": "Yes", "gnf": "Yes"},
    # "roa" is a nonstandard variant of "rup".
    "roa": {"name": "Aromanian", "fs": "Yes", "gnf": "Yes"},
    # "roa-rup" is a nonstandard variant of "rup".
    "roa-rup": {"name": "Aromanian", "fs": "Yes", "gnf": "Yes"},
    # "roa-tara" is a nonstandardized code.
    "roa-tara": {"name": "Tarantino", "fs": "Yes", "gnf": "Yes"},
    "ru": {"name": "Russian", "fs": "Yes", "gnf": "Yes"},
    "rue": {"name": "Rusyn", "fs": "Yes", "gnf": "Yes"},
    "rup": {"name": "Aromanian", "fs": "Yes", "gnf": "Yes"},
    "rw": {"name": "Kinyarwanda", "fs": "Yes", "gnf": "Yes"},
    "sa": {"name": "Sanskrit", "fs": "No", "gnf": "idk"},
    "sah": {"name": "Sakha", "fs": "Yes", "gnf": "No"},
    "sat": {"name": "Santali", "fs": "No", "gnf": "idk"},
    "sc": {"name": "Sardinian", "fs": "Yes", "gnf": "Yes"},
    "scn": {"name": "Sicilian", "fs": "Yes", "gnf": "Yes"},
    "sco": {"name": "Scots", "fs": "Yes", "gnf": "Yes"},
    "sd": {"name": "Sindhi", "fs": "Yes", "gnf": "Yes"},
    "se": {"name": "Northern Sami", "fs": "Yes", "gnf": "Yes"},
    "sg": {"name": "Sango", "fs": "Yes", "gnf": "Yes"},
    "sgs": {"name": "Samogitian", "fs": "Yes", "gnf": "Yes"},
    "sh": {"name": "Serbo-Croatian", "fs": "Yes", "gnf": "Yes"},
    "shn": {"name": "Shan", "fs": "No", "gnf": "idk"},
    "si": {"name": "Sinhalese", "fs": "No", "gnf": "idk"},
    # "simple" is a nonstandard variant of "en-simple".
    "simple": {"name": "Simple English", "fs": "Yes", "gnf": "Yes"},
    "sk": {"name": "Slovak", "fs": "Yes", "gnf": "Yes"},
    "sl": {"name": "Slovene", "fs": "Yes", "gnf": "Yes"},
    "sm": {"name": "Samoan", "fs": "Yes", "gnf": "Yes"},
    "sn": {"name": "Shona", "fs": "Yes", "gnf": "Yes"},
    "so": {"name": "Somali", "fs": "Yes", "gnf": "Yes"},
    "sq": {"name": "Albanian", "fs": "Yes", "gnf": "Yes"},
    "sr": {"name": "Serbian", "fs": "Yes", "gnf": "Yes"},
    "srn": {"name": "Sranan Tongo", "fs": "Yes", "gnf": "Yes"},
    "ss": {"name": "Swati", "fs": "Yes", "gnf": "No"},
    "st": {"name": "Sesotho", "fs": "Yes", "gnf": "Yes"},
    "stq": {"name": "Saterland Frisian", "fs": "Yes", "gnf": "Yes"},
    "su": {"name": "Sundanese", "fs": "Yes", "gnf": "Yes"},
    "sv": {"name": "Swedish", "fs": "Yes", "gnf": "Yes"},
    "sw": {"name": "Swahili", "fs": "Yes", "gnf": "Yes"},
    "szl": {"name": "Silesian", "fs": "Yes", "gnf": "Yes"},
    "szy": {"name": "Sakizaya", "fs": "Yes", "gnf": "Yes"},
    "ta": {"name": "Tamil", "fs": "No", "gnf": "idk"},
    "tcy": {"name": "Tulu", "fs": "No", "gnf": "idk"},
    "te": {"name": "Telugu language", "fs": "No", "gnf": "idk"},
    "tet": {"name": "Tetum", "fs": "Yes", "gnf": "Yes"},
    "tg": {"name": "Tajik", "fs": "Yes", "gnf": "Yes"},
    "th": {"name": "Thai", "fs": "No", "gnf": "idk"},
    "ti": {"name": "Tigrinya", "fs": "No", "gnf": "idk"},
    "tk": {"name": "Turkmen", "fs": "Yes", "gnf": "Yes"},
    "tl": {"name": "Tagalog", "fs": "Yes", "gnf": "Yes"},
    "tn": {"name": "Tswana", "fs": "Yes", "gnf": "Yes"},
    "to": {"name": "Tongan", "fs": "Yes", "gnf": "Yes"},
    "tpi": {"name": "Tok Pisin", "fs": "Yes", "gnf": "Yes"},
    "tr": {"name": "Turkish", "fs": "Yes", "gnf": "No"},
    "ts": {"name": "Tsonga", "fs": "Yes", "gnf": "Yes"},
    "tt": {"name": "Tatar", "fs": "Yes", "gnf": "No"},
    "tum": {"name": "Tumbuka", "fs": "Yes", "gnf": "Yes"},
    "tw": {"name": "Twi", "fs": "Yes", "gnf": "Yes"},
    "ty": {"name": "Tahitian", "fs": "Yes", "gnf": "Yes"},
    "tyv": {"name": "Tuvan", "fs": "Yes", "gnf": "Yes"},
    "udm": {"name": "Udmurt", "fs": "Yes", "gnf": "No"},
    "ug": {"name": "Uyghur", "fs": "Yes", "gnf": "Yes"},
    "uk": {"name": "Ukrainian", "fs": "Yes", "gnf": "Yes"},
    "ur": {"name": "Urdu", "fs": "Yes", "gnf": "Yes"},
    "uz": {"name": "Uzbek", "fs": "Yes", "gnf": "No"},
    "ve": {"name": "Venda", "fs": "Yes", "gnf": "Yes"},
    "vec": {"name": "Venetian", "fs": "Yes", "gnf": "Yes"},
    "vep": {"name": "Veps", "fs": "Yes", "gnf": "Yes"},
    "vi": {"name": "Vietnamese", "fs": "Yes", "gnf": "Yes"},
    "vls": {"name": "West Flemish", "fs": "Yes", "gnf": "Yes"},
    "vo": {"name": "Volapük", "fs": "Yes", "gnf": "Yes"},
    "vro": {"name": "Võro", "fs": "Yes", "gnf": "Yes"},
    "wa": {"name": "Walloon", "fs": "Yes", "gnf": "Yes"},
    "war": {"name": "Waray", "fs": "Yes", "gnf": "Yes"},
    "wo": {"name": "Wolof", "fs": "Yes", "gnf": "Yes"},
    "wuu": {"name": "Wu", "fs": "No", "gnf": "idk"},
    "xal": {"name": "Kalmyk", "fs": "Yes", "gnf": "No"},
    "xh": {"name": "Xhosa", "fs": "Yes", "gnf": "Yes"},
    "xmf": {"name": "Mingrelian", "fs": "No", "gnf": "idk"},
    "yi": {"name": "Yiddish", "fs": "No", "gnf": "idk"},
    "yo": {"name": "Yoruba", "fs": "Yes", "gnf": "Yes"},
    "yue": {"name": "Cantonese", "fs": "No", "gnf": "idk"},
    "za": {"name": "Zhuang", "fs": "Yes", "gnf": "Yes"},
    "zea": {"name": "Zealandic", "fs": "Yes", "gnf": "Yes"},
    "zh": {"name": "Chinese", "fs": "No", "gnf": "idk"},
    # "zh-classical" is a nonstandard variant of "lzh".
    "zh-classical": {"name": "Classical Chinese", "fs": "No",
                     "gnf": "idk"},
    # "zh-min-nan" is a nonstandard variant of "nan".
    "zh-min-nan": {"name": "Min Nan", "fs": "Yes", "gnf": "Yes"},
    # "zh-yue" is a nonstandard variant of "yue".
    "zh-yue": {"name": "Cantonese", "fs": "No", "gnf": "idk"},
    "zu": {"name": "Zulu", "fs": "Yes", "gnf": "Yes"}
    }

for english_dict in english_dicts:
    # Scrape each URL added above.
    url = english_dict["URL"]
    res = requests.get(url)
    data = res.text
    soup = BeautifulSoup(data, "lxml")
    # Find all <a> tags for interlanguage links.
    tags = soup.find_all("a", {"class": "interlanguage-link-target"})
    for tag in tags:
        try:
            title = tag["title"]
            if title is not None:
                # Remove en dashes and following text from titles. For
                #   instance, if the title is "Alfred le Grand –
                #   French", change it to "Alfred le Grand".
                en_dash = title.find("–")
                if en_dash > 0:
                    title = title[:en_dash-1]
                # Remove parenthetical text from titles. For instance,
                #   if the title is "Henri Ier (roi d'Angleterre)",
                #   change it to "Henri Ier".
                paren = title.find("(")
                if paren > 0:
                    title = title[:paren-1]
                # Remove commas and following text from titles. For
                #   instance, if the title is "Vilim I, kralj Engleske",
                #   change it to "Vilim I".
                comma = title.find(",")
                if comma > 0:
                    title = title[:comma]
                # Get the first word of the title.
                space = title.find(" ")
                if space > 0:
                    first_word = title[:space]
                else:
                    first_word = title
                all_dicts.append({
                    "Name (English)": english_dict["Name (English)"],
                    "Full Name (English)": english_dict[
                        "Full Name (English)"],
                    "URL": english_dict["URL"],
                    "Language": language_tags[tag["lang"]]["name"],
                    "Name": first_word,
                    "Full Name": title,
                    "Familiar-ish Script": language_tags[
                        tag["lang"]]["fs"],
                    "Given Name Usually First": language_tags[
                        tag["lang"]]["gnf"]
                    })
        except:
            continue      

# Change to the directory in which to save the csv.
os.chdir("C:/Users/username/Documents")
# Create a dataframe out of dicts.
df = pd.DataFrame(all_dicts)
# Write the dataframe to csv.
df.to_csv("english_monarchs.csv", encoding="utf-8-sig")

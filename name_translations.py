#! python3
# name_translations.py

"""
This program produces a csv with translations of people's names. It
    scrapes Wikipedia lists that tend to include people who lived in
    ancient, medieval, or early modern times, since their names are more
    likely to be translated than are names of contemporary people. It
    includes names from the following lists:

        List of Belgian monarchs
        List of Catholic saints
        List of Coptic Orthodox popes of Alexandria
        List of Danish monarchs
        List of English monarchs
        List of female hereditary rulers
        List of female mystics
        List of female scientists before the 20th century
        List of French monarchs
        List of German monarchs
        List of major biblical figures
        List of monarchs of Georgia
        List of Norwegian monarchs
        List of popes
        List of Portuguese monarchs
        List of prostitutes and courtesans
        List of Roman women
        List of rulers of Iceland
        List of rulers of Monaco
        List of saints
        List of Scottish royal mistresses
        List of Spanish monarchs
        List of sultans of the Ottoman Empire
        List of Swedish royal mistresses
        List of women in the Bible
        List of women warriors in folklore
        List of women who led a revolt or rebellion
        Women as theological figures

The program returns some entries for nonhuman entities, but most entries
    are for humans.

This program takes about 25 minutes to run.
"""

# Import libraries.
import requests
from bs4 import BeautifulSoup
import os
import pandas as pd

# Create a list of Wikipedia lists in which most links of interest
#   appear in the first columns of tables.
urls_first_columns = {
    "https://en.wikipedia.org/wiki/List_of_Belgian_monarchs":
        "List of Belgian monarchs",
    "https://en.wikipedia.org/wiki/List_of_Catholic_saints":
        "List of Catholic saints",
    "https://en.wikipedia.org/wiki/List_of_Danish_monarchs":
        "List of Danish monarchs",
    "https://en.wikipedia.org/wiki/List_of_English_monarchs":
        "List of English monarchs",
    "https://en.wikipedia.org/wiki/List_of_monarchs_of_Georgia":
        "List of monarchs of Georgia",
    "https://en.wikipedia.org/wiki/List_of_Norwegian_monarchs":
        "List of Norwegian monarchs",
    "https://en.wikipedia.org/wiki/List_of_Portuguese_monarchs":
        "List of Portuguese monarchs",
    "https://en.wikipedia.org/wiki/List_of_Roman_women":
        "List of Roman women",
    "https://en.wikipedia.org/wiki/List_of_rulers_of_Iceland":
        "List of rulers of Iceland",
    "https://en.wikipedia.org/wiki/List_of_rulers_of_Monaco":
        "List of rulers of Monaco",
    "https://en.wikipedia.org/wiki/List_of_saints":
        "List of saints",
    "https://en.wikipedia.org/wiki/List_of_Spanish_monarchs":
        "List of Spanish monarchs",
    "https://en.wikipedia.org/wiki/List_of_sultans_of_the_Ottoman_Empire":
        "List of sultans of the Ottoman Empire"
    }

# Create a list of Wikipedia lists in which most links of interest
#   appear in wikitables, but not consistently in any particular column.
urls_all_table_links = {
    "https://en.wikipedia.org/wiki/" +
        "List_of_Coptic_Orthodox_popes_of_Alexandria":
        "List of Coptic Orthodox popes of Alexandria",
    "https://en.wikipedia.org/wiki/List_of_French_monarchs":
        "List of French monarchs",
    "https://en.wikipedia.org/wiki/List_of_German_monarchs":
        "List of German monarchs",
    "https://en.wikipedia.org/wiki/List_of_popes":
        "List of popes"
    }

# Create a list of Wikipedia lists in which most links of interest
#   appear as the first link in a list item.
urls_first_li_links = {
    "https://en.wikipedia.org/wiki/List_of_female_hereditary_rulers":
        "List of female hereditary rulers",
    "https://en.wikipedia.org/wiki/List_of_female_mystics":
        "List of female mystics",
    "https://en.wikipedia.org/wiki/" +
        "List_of_female_scientists_before_the_20th_century":
        "List of female scientists before the 20th century",
    "https://en.wikipedia.org/wiki/List_of_prostitutes_and_courtesans":
        "List of prostitutes and courtesans",
    "https://en.wikipedia.org/wiki/List_of_women_in_the_Bible":
        "List of women in the Bible",
    "https://en.wikipedia.org/wiki/List_of_Roman_women":
        "List of Roman women",
    "https://en.wikipedia.org/wiki/List_of_Scottish_royal_mistresses":
        "List of Scottish royal mistresses",
    "https://en.wikipedia.org/wiki/List_of_Swedish_royal_mistresses":
        "List of Swedish royal mistresses",
    "https://en.wikipedia.org/wiki/List_of_women_warriors_in_folklore":
        "List of women warriors in folklore",
    "https://en.wikipedia.org/wiki/" +
        "List_of_women_who_led_a_revolt_or_rebellion":
        "List of women who led a revolt or rebellion",
    "https://en.wikipedia.org/wiki/Women_as_theological_figures":
        "Women as theological figures"
    }

# Create a list of Wikipedia lists for which it is necessary to get all
#   links to get items of interest.
urls_all_links = {
    "https://en.wikipedia.org/wiki/List_of_major_biblical_figures":
        "List of major biblical figures"
    }


# Create a list to which to add dictionaries for the English language
#   pages for all selected list items. The dictionary keys will be the
#   URLs that will later be scraped for name translations.
english_dicts = []

# Create a list to which to add dictionaries for pages in any language
#   for all selected list items. This is what will eventually be written
#   to a csv file.
all_dicts = []

# Create a list to which to add hrefs for the English language pages of
#   all selected list items. Hrefs will serve as unique identifiers for
#   the list items. This list will be used to avoid duplicate entries.
#   I'll provide two examples of duplicate entries that this list will
#   avoid: Æthelred the Unready was a monarch who had two reigns and
#   thus is listed twice on Wikipedia's "List of English monarchs".
#   Sweyn Forkbeard was a Danish monarch who controlled England for a
#   time, and thus is listed both on Wikipedia's "List of English
#   monarchs" and on its "List of Danish monarchs".
hrefs = []

# Create a list to which to add dictionaries that include links of
#   interest and BeautifulSoup result sets for each of the pages listed
#   above.
result_sets = []

# Scrape each of the URLs listed in first_column_urls.
for url_fc in urls_first_columns:
    url = url_fc
    res = requests.get(url)
    data = res.text
    soup = BeautifulSoup(data, "lxml")
    # Create a dictionary with the name of the scraped page as the key
    #   and, as the value, a BeautifulSoup result set created from the
    #   first columns of the pages tables.
    result_sets.append({urls_first_columns[url_fc]:
                            soup.select("table tr td:nth-of-type(1)")})

# Scrape each of the URLs listed in urls_all_table_links.
for url_tl in urls_all_table_links:
    url = url_tl
    res = requests.get(url)
    data = res.text
    soup = BeautifulSoup(data, "lxml")
    # Create a dictionary with the name of the scraped page as the key
    #   and, as the value, a BeautifulSoup result set of all the page's
    #   wikitables.
    result_sets.append({urls_all_table_links[url_tl]:
                            soup.find_all("table",
                                          {"class": "wikitable"})})

# Scrape each of the URLs listed in urls_first_li_links.
for url_li in urls_first_li_links:
    url = url_li
    res = requests.get(url)
    data = res.text
    soup = BeautifulSoup(data, "lxml")
    # Create a dictionary with the name of the scraped page as the key
    #   and, as the value, a BeautifulSoup result set from all first
    #   links in the page's list items.
    result_sets.append({urls_first_li_links[url_li]:
                            soup.select("li a:nth-of-type(1)")})

# Scrape each of the URLs listed in urls_all_links.
for url_al in urls_all_links:
    url = url_al
    res = requests.get(url)
    data = res.text
    soup = BeautifulSoup(data, "lxml")
    # Create a dictionary with the name of the scraped page as the key
    #   and, as the value, a BeautifulSoup result set from all links on
    #   the page.
    result_sets.append({urls_all_links[url_al]:
                            soup.find_all("a")})

# Get all <a> tags from the result sets in result_sets. For each <a>
#   tag, add the link and title to a dictionary for the monarch.
for dict in result_sets:
    for key in dict:
        for item in dict[key]:
            tags = item.find_all("a")
            for tag in tags:
                href = tag.get("href")
                if href not in hrefs:
                    if href is not None:
                        if href.startswith("/wiki/"):
                            if not href.startswith("/wiki/File"):
                                hrefs.append(href)
                                title = tag.get("title")
                                if title is not None:
                                    # Remove en dashes and following
                                    #   text from titles. For instance,
                                    #   if the title is "Alfred le Grand
                                    #   - French", change it to "Alfred
                                    #   le Grand".
                                    en_dash = title.find("–")
                                    if en_dash > 0:
                                        title = title[:en_dash-1]
                                    # Remove parenthetical text from
                                    #   titles. For instance, if the
                                    #   title is "Henry Ier (roi
                                    #   d'Angleterre)", change it to
                                    #   "Henri Ier".
                                    paren = title.find("(")
                                    if paren > 0:
                                        title = title[:paren-1]
                                    # Remove commas and following text
                                    #   from titles. For instance, if
                                    #   the title is "Vilim I, kralj
                                    #   Engleske", change it to "Vilim
                                    #   I".
                                    comma = title.find(",")
                                    if comma > 0:
                                        title = title[:comma]
                                    # Get the first word of the title.
                                    space = title.find(" ")
                                    if space > 0:
                                        title_first_word = title[:space]
                                    else:
                                        title_first_word = title
                                    # Create a dictionary for the page.
                                    href = {
                                        "Name (English)": title_first_word,
                                        "Full Name (English)": title,
                                        "URL": "https://en.wikipedia.org" +
                                            href,
                                        "Language": "English",
                                        "Name": title_first_word,
                                        "Full Name": title,
                                        "Familiar-ish Script": "Yes",
                                        "Given Name Usually First": "Yes",
                                        "Source": key
                                        }
                                    # Add the newly-created dictionary
                                    #   to the lists.
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
                        tag["lang"]]["gnf"],
                    "Source": english_dict["Source"]
                    })
        except:
            continue

# Change to the directory in which to save the csv.
os.chdir("C:/Users/username//Documents")
# Create a dataframe out of dicts.
df = pd.DataFrame(all_dicts)
# Write the dataframe to csv.
df.to_csv("name_translations.csv", encoding="utf-8-sig")

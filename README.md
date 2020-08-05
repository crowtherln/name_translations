# name_translations

This is a project to find translations of people's given names. To do
    this, I scrape Wikipedia lists that tend to include people who
    lived in ancient, medieval, or early modern times, since their
    names are more likely to be translated than are names of
    contemporary people. The programs produce csv files of which given
    names in English correspond to which given names in other
    languages.

english_monarchs.py does this for English monarchs and takes about 55
    seconds to run. The raw, uncleaned results from that program are in
    english_monarch_name_translations.csv.

name_translations.py does it for that and 27 other lists; it takes
    about 25 minutes to run. The raw, uncleaned results from that
    program are in a csv file in name_translations.zip.

These programs return some entries for nonhuman entities, but most
    entries are for humans.

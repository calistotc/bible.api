import json
import os

from .score_search import score_search


BOOKS = []
# Get the path relative to this file
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
with open(os.path.join(DATA_DIR, "translations_books.json")) as json_file:
    BOOKS = json.load(json_file)


triple_shortcuts = {
    "GEN": 1,
    "EXO": 2,
    "LEV": 3,
    "NUM": 4,
    "DEU": 5,
    "JOS": 6,
    "JDG": 7,
    "RUT": 8,
    "1SA": 9,
    "2SA": 10,
    "1KI": 11,
    "2KI": 12,
    "1CH": 13,
    "2CH": 14,
    "EZR": 15,
    "NEH": 16,
    "EST": 17,
    "JOB": 18,
    "PSA": 19,
    "PRO": 20,
    "ECC": 21,
    "SNG": 22,
    "ISA": 23,
    "JER": 24,
    "LAM": 25,
    "EZK": 26,
    "DAN": 27,
    "HOS": 28,
    "JOL": 29,
    "AMO": 30,
    "OBA": 31,
    "JON": 32,
    "MIC": 33,
    "NAM": 34,
    "HAB": 35,
    "ZEP": 36,
    "HAG": 37,
    "ZEC": 38,
    "MAL": 39,
    "MAT": 40,
    "MRK": 41,
    "LUK": 42,
    "JHN": 43,
    "ACT": 44,
    "ROM": 45,
    "1CO": 46,
    "2CO": 47,
    "GAL": 48,
    "EPH": 49,
    "PHP": 50,
    "COL": 51,
    "1TH": 52,
    "2TH": 53,
    "1TI": 54,
    "2TI": 55,
    "TIT": 56,
    "PHM": 57,
    "HEB": 58,
    "JAS": 59,
    "1PE": 60,
    "2PE": 61,
    "1JN": 62,
    "2JN": 63,
    "3JN": 64,
    "JUD": 65,
    "REV": 66,
}

# User-friendly book codes (mixed case, more intuitive)
friendly_shortcuts = {
    "GEN": 1, "Gen": 1, "GENESIS": 1, "Genesis": 1,
    "EXO": 2, "Exo": 2, "EXODUS": 2, "Exodus": 2,
    "LEV": 3, "Lev": 3, "LEVITICUS": 3, "Leviticus": 3,
    "NUM": 4, "Num": 4, "NUMBERS": 4, "Numbers": 4,
    "DEU": 5, "Deu": 5, "DEUTERONOMY": 5, "Deuteronomy": 5,
    "JOS": 6, "Jos": 6, "JOSHUA": 6, "Joshua": 6,
    "JDG": 7, "Jdg": 7, "JUDGES": 7, "Judges": 7,
    "RUT": 8, "Rut": 8, "RUTH": 8, "Ruth": 8,
    "1SA": 9, "1Sa": 9, "1SAMUEL": 9, "1Samuel": 9, "1 Samuel": 9,
    "2SA": 10, "2Sa": 10, "2SAMUEL": 10, "2Samuel": 10, "2 Samuel": 10,
    "1KI": 11, "1Ki": 11, "1KINGS": 11, "1Kings": 11, "1 Kings": 11,
    "2KI": 12, "2Ki": 12, "2KINGS": 12, "2Kings": 12, "2 Kings": 12,
    "1CH": 13, "1Ch": 13, "1CHRONICLES": 13, "1Chronicles": 13, "1 Chronicles": 13,
    "2CH": 14, "2Ch": 14, "2CHRONICLES": 14, "2Chronicles": 14, "2 Chronicles": 14,
    "EZR": 15, "Ezr": 15, "EZRA": 15, "Ezra": 15,
    "NEH": 16, "Neh": 16, "NEHEMIAH": 16, "Nehemiah": 16,
    "EST": 17, "Est": 17, "ESTHER": 17, "Esther": 17,
    "JOB": 18, "Job": 18,
    "PSA": 19, "Psa": 19, "PS": 19, "Ps": 19, "PSALM": 19, "Psalm": 19, "PSALMS": 19, "Psalms": 19,
    "PRO": 20, "Pro": 20, "PROVERBS": 20, "Proverbs": 20,
    "ECC": 21, "Ecc": 21, "ECCLESIASTES": 21, "Ecclesiastes": 21,
    "SNG": 22, "Sng": 22, "SONG": 22, "Song": 22, "SONG OF SOLOMON": 22, "Song of Solomon": 22, "SONG OF SONGS": 22, "Song of Songs": 22,
    "ISA": 23, "Isa": 23, "ISAIAH": 23, "Isaiah": 23,
    "JER": 24, "Jer": 24, "JEREMIAH": 24, "Jeremiah": 24,
    "LAM": 25, "Lam": 25, "LAMENTATIONS": 25, "Lamentations": 25,
    "EZK": 26, "Ezk": 26, "EZE": 26, "Eze": 26, "EZEKIEL": 26, "Ezekiel": 26,
    "DAN": 27, "Dan": 27, "DANIEL": 27, "Daniel": 27,
    "HOS": 28, "Hos": 28, "HOSEA": 28, "Hosea": 28,
    "JOL": 29, "Joe": 29, "Joel": 29, "JOEL": 29,
    "AMO": 30, "Amo": 30, "Amos": 30, "AMOS": 30,
    "OBA": 31, "Oba": 31, "Obadiah": 31, "OBADIAH": 31,
    "JON": 32, "Jon": 32, "Jonah": 32, "JONAH": 32,
    "MIC": 33, "Mic": 33, "Micah": 33, "MICAH": 33,
    "NAM": 34, "Nam": 34, "Nah": 34, "Nahum": 34, "NAHUM": 34,
    "HAB": 35, "Hab": 35, "Habakkuk": 35, "HABAKKUK": 35,
    "ZEP": 36, "Zep": 36, "Zephaniah": 36, "ZEPHANIAH": 36,
    "HAG": 37, "Hag": 37, "Haggai": 37, "HAGGAI": 37,
    "ZEC": 38, "Zec": 38, "Zechariah": 38, "ZECHARIAH": 38,
    "MAL": 39, "Mal": 39, "Malachi": 39, "MALACHI": 39,
    "MAT": 40, "Mat": 40, "Matt": 40, "MATT": 40, "MATTHEW": 40, "Matthew": 40,
    "MRK": 41, "Mrk": 41, "Mark": 41, "MARK": 41,
    "LUK": 42, "Luk": 42, "Luke": 42, "LUKE": 42,
    "JHN": 43, "Jhn": 43, "John": 43, "JOHN": 43,
    "ACT": 44, "Act": 44, "Acts": 44, "ACTS": 44,
    "ROM": 45, "Rom": 45, "Romans": 45, "ROMANS": 45,
    "1CO": 46, "1Co": 46, "1COR": 46, "1Cor": 46, "1CORINTHIANS": 46, "1Corinthians": 46, "1 Corinthians": 46,
    "2CO": 47, "2Co": 47, "2COR": 47, "2Cor": 47, "2CORINTHIANS": 47, "2Corinthians": 47, "2 Corinthians": 47,
    "GAL": 48, "Gal": 48, "Galatians": 48, "GALATIANS": 48,
    "EPH": 49, "Eph": 49, "Ephesians": 49, "EPHESIANS": 49,
    "PHP": 50, "Php": 50, "Phil": 50, "PHIL": 50, "Philippians": 50, "PHILIPPIANS": 50,
    "COL": 51, "Col": 51, "Colossians": 51, "COLOSSIANS": 51,
    "1TH": 52, "1Th": 52, "1THESS": 52, "1Thess": 52, "1THESSALONIANS": 52, "1Thessalonians": 52, "1 Thessalonians": 52,
    "2TH": 53, "2Th": 53, "2THESS": 53, "2Thess": 53, "2THESSALONIANS": 53, "2Thessalonians": 53, "2 Thessalonians": 53,
    "1TI": 54, "1Ti": 54, "1TIM": 54, "1Tim": 54, "1TIMOTHY": 54, "1Timothy": 54, "1 Timothy": 54,
    "2TI": 55, "2Ti": 55, "2TIM": 55, "2Tim": 55, "2TIMOTHY": 55, "2Timothy": 55, "2 Timothy": 55,
    "TIT": 56, "Tit": 56, "TITUS": 56, "Titus": 56,
    "PHM": 57, "Phm": 57, "Philemon": 57, "PHILEMON": 57,
    "HEB": 58, "Heb": 58, "Hebrews": 58, "HEBREWS": 58,
    "JAS": 59, "Jas": 59, "James": 59, "JAMES": 59,
    "1PE": 60, "1Pe": 60, "1PET": 60, "1Pet": 60, "1PETER": 60, "1Peter": 60, "1 Peter": 60,
    "2PE": 61, "2Pe": 61, "2PET": 61, "2Pet": 61, "2PETER": 61, "2Peter": 61, "2 Peter": 61,
    "1JN": 62, "1Jn": 62, "1JOHN": 62, "1John": 62, "1 John": 62,
    "2JN": 63, "2Jn": 63, "2JOHN": 63, "2John": 63, "2 John": 63,
    "3JN": 64, "3Jn": 64, "3JOHN": 64, "3John": 64, "3 John": 64,
    "JUD": 65, "Jud": 65, "Jude": 65, "JUDE": 65,
    "REV": 66, "Rev": 66, "Revelation": 66, "REVELATION": 66,
}

twin_shortcuts = {
    "GN": 1,
    "EX": 2,
    "LV": 3,
    "NU": 4,
    "DT": 5,
    "JS": 6,
    "JG": 7,
    "RT": 8,
    "S1": 9,
    "S2": 10,
    "K1": 11,
    "K2": 12,
    "R1": 13,
    "R2": 14,
    "ER": 15,
    "NH": 16,
    "ET": 17,
    "JB": 18,
    "PS": 19,
    "PR": 20,
    "EC": 21,
    "SS": 22,
    "IS": 23,
    "JR": 24,
    "LM": 25,
    "EK": 26,
    "DN": 27,
    "HS": 28,
    "JL": 29,
    "AM": 30,
    "OB": 31,
    "JH": 32,
    "MC": 33,
    "NM": 34,
    "HK": 35,
    "ZP": 36,
    "HG": 37,
    "ZC": 38,
    "ML": 39,
    "MT": 40,
    "MK": 41,
    "LK": 42,
    "JN": 43,
    "AC": 44,
    "RM": 45,
    "C1": 46,
    "C2": 47,
    "GL": 48,
    "EP": 49,
    "PP": 50,
    "CL": 51,
    "H1": 52,
    "H2": 53,
    "T1": 54,
    "T2": 55,
    "TT": 56,
    "PM": 57,
    "HB": 58,
    "JM": 59,
    "P1": 60,
    "P2": 61,
    "J1": 62,
    "J2": 63,
    "J3": 64,
    "JD": 65,
    "RV": 66,
}


def is_number(n):
    if isinstance(n, (int, float, complex)):
        return True
    try:
        int(n)
        return True
    except ValueError:
        return False


def get_book_id(translation, book_slug):
    # if book_slug is already a number return it
    if is_number(book_slug):
        return int(book_slug)

    # Check friendly shortcuts first (supports mixed case and full names)
    if book_slug in friendly_shortcuts:
        return friendly_shortcuts[book_slug]

    book_slug_upper = book_slug.upper()

    if book_slug_upper in triple_shortcuts:
        return triple_shortcuts[book_slug_upper]
    if book_slug_upper in twin_shortcuts:
        return twin_shortcuts[book_slug_upper]

    book_slug = book_slug.lower()

    suggestions = []
    for b in BOOKS[translation]:
        if b["name"].lower() == book_slug:
            return b["bookid"]
        score = score_search(b["name"], book_slug)
        if score:
            suggestions.append((b, score))
    suggestions.sort(key=lambda x: x[1], reverse=True)
    if len(suggestions) > 0:
        return suggestions[0][0]["bookid"]

    raise ValueError(
        f"Book '{book_slug}' not found in translation '{translation}'. "
        f"Please check the book name or use a different translation."
    )


# print(get_book_id("KJV", "ot"))
# print(get_book_id("KJV", "jo"))
# print(get_book_id("KJV", "gen"))
# print(get_book_id("KJV", "Matthaw"))
# print(get_book_id("ESV", "Genesis"))
# print(get_book_id("ESV", "Acts"))

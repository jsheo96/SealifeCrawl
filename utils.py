# Function which distinguishes a string contains date. e.g., 2022-08-10
# Source: https://stackoverflow.com/questions/25341945/check-if-string-has-date-any-format

from dateutil.parser import parse
import re

def is_date(string, fuzzy=False):
    """
    Return whether the string can be interpreted as a date.

    :param string: str, string to check for date
    :param fuzzy: bool, ignore unknown tokens in string if True
    """
    string = string.replace(' ', '')
    if re.fullmatch(r'(\d+(,\d{3})+)|\d{1,5}|\d{7}|\d{9,}', string): # Only number like 1,234 or 123 is not a date
        return False
    try:
        parse(string, fuzzy=fuzzy)
        return True

    except ValueError:
        return False
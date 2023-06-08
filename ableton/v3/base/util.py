from __future__ import absolute_import, print_function, unicode_literals
from . import is_iterable

def get_default_ascii_translations():
    ascii_translations = {chr(i): i for i in range(32, 127)}
    ascii_translations['♯'] = 35
    return ascii_translations


DEFAULT_ASCII_TRANSLATIONS = get_default_ascii_translations()

def as_ascii(string, ascii_translations=DEFAULT_ASCII_TRANSLATIONS):
    result = []
    for char in string:
        translated_char = ascii_translations.get(char, ascii_translations['?'])
        if is_iterable(translated_char):
            result.extend(translated_char)
        else:
            result.append(translated_char)

    return result


def hex_to_rgb(hex_value):
    return (
     (hex_value & 16711680) >> 16,
     (hex_value & 65280) >> 8,
     hex_value & 255)
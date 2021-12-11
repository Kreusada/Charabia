"""Charabia - French for gibberish. Another reversible encryption based encoder.

decode() - decode Charabia into standard text.
encode() - encode a string into Charabia.
"""

__all__ = [
    "CharabiaError",
    "__all__",
    "__version__",
    "decode",
    "encode",
]

import string

_letters = string.ascii_lowercase[:10]
_letters_dict = dict(zip(_letters, range(0, 10)))
_getstr = lambda n: "".join(map(_letters.__getitem__, map(int, str(n))))
__version__ = "1.0.0"

class CharabiaError(Exception):
    pass


def encode(s: str):
    """Encode a string into Charabia."""
    return "k".join(map(_getstr, tuple(map(ord, s))))


def decode(s: str):
    """Decode Charabia into standard text."""
    split = s.strip("k").strip().split("k")

    def getint(s: str):
        try:
            return int("".join(map(str, (map(_letters_dict.__getitem__, s)))))
        except KeyError as e:
            raise CharabiaError(f"invalid identifier: {e}") from None

    for i in (m := tuple(map(getint, split))) :
        if not i in range(0x110000):
            raise CharabiaError(f"invalid identifier: '{_getstr(i)}'") from None
    return "".join(map(chr, m))


def main():
    print("Encode or decode?")
    while True:
        opt = input(">>> ").lower()
        if opt in ("encode", "decode"):
            break
        print("Please provide 'encode' or 'decode'.")
        continue
    text = input("Provide text:\n>>> ")

    try:
        if opt == "encode":
            print(encode(text))
        else:
            print(decode(text))
    except CharabiaError as e:
        print(str(e))


if __name__ == "__main__":
    main()

del string
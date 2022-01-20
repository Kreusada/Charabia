"""
Library designed for reversible sheltering of sensitive information/data,
meaning you can shelter strings or tokens using this encoder.
"""

import contextlib
import functools
import string
import random
import re
import types
from typing import Dict, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from types import FunctionType

SEPS = None
ENCODING_INDEXES = None
DECODING_INDEXES = None
__version__ = "2.0.0"

__all__ = (
    "CharabiaError"
    "__version__",
    "configured",
    "create_tower",
    "decode",
    "demolish_tower",
    "encode",
    "ensure_setsep",
    "generate_decoding_indexes",
    "generate_encoding_indexes",
    "getseps",
    "setseps",
    "splitseps",
    "tempseps",
)


class CharabiaError(Exception):
    """Charabia related errors."""


def _parse_separators(separators) -> None:
    if not isinstance(separators, str):
        raise TypeError("separators must be provided as str")
    if 1 > len(separators) > 42:
        raise ValueError("separators length must be between 1 and 42")
    if not separators.isalnum():
        raise ValueError("all separators must be alphanumeric")


def setseps(separators: str) -> None:
    """Configure separators.

    Parameters
    ----------
    separators: str
        The separators to configure. Must be alphanumeric and provided
        string length must be between 1 and 42.
    """
    _parse_separators(separators)
    global SEPS
    global ENCODING_INDEXES
    global DECODING_INDEXES
    SEPS = "".join(list(dict.fromkeys(separators)))
    ENCODING_INDEXES = generate_encoding_indexes(SEPS)
    DECODING_INDEXES = generate_decoding_indexes(SEPS)


def getseps() -> Optional[str]:
    """Get the separator configuration for charabia."""
    return SEPS


def generate_encoding_indexes(seps) -> Dict[int, List[str]]:
    """Generate encoding indexes for the provided separators."""
    return {
        n: [j for i, j in enumerate(string.ascii_letters) if (i % 10 == n and j not in seps)]
        for n in range(10)
    }


def generate_decoding_indexes(seps) -> Dict[str, str]:
    """Generate decoding indexes for the provided separators."""
    return dict(
        {i: str(k) for k, v in generate_encoding_indexes(seps).items() for i in v},
        **{sep: " " for sep in seps},
        **{"\n": ""},
    )


def ensure_setsep(f) -> FunctionType:
    @functools.wraps(f)
    def inner(*args, **kwargs):
        if not configured():
            raise RuntimeError(
                "separators have not been declared, or the configuration has been damaged (please use setseps())"
            )
        return f(*args, **kwargs)

    return inner


def configured() -> bool:
    """Returns whether charabia is fully configured and safe for encoding/decoding."""
    return all([SEPS, ENCODING_INDEXES, DECODING_INDEXES])


def create_tower(string: str, tower_rows: int) -> str:
    """Creates a tower for a given string.

    Parameters
    ----------
    string: str
        The string to build the tower upon.

    tower_rows: str
        Characters per line, separated by a line break. Set to 0 to
        disable linewrapping entirely.

    Returns
    -------
    str
        The tower string.
    """
    if not tower_rows:
        if "\n" in string:
            string = "".join(string.split("\n"))
        return string
    return "\n".join([string[x : x + tower_rows] for x in range(0, len(string), tower_rows)])


def demolish_tower(string: str) -> str:
    """Demolishes a tower from a given string.

    Parameters
    ----------
    string: str
        The string to demolish the tower from.

    Returns
    -------
    str
        The demolished string.
    """
    return create_tower(string, 0)


def _encode(text: str, seed: bool):
    if seed:
        func = random.choice
    else:
        func = lambda x: x[0]
    joinords = lambda n: "".join(map(lambda x: func(ENCODING_INDEXES[x]), map(int, str(n))))
    compiled = list(map(joinords, map(ord, text)))
    return "".join(
        f"{j}{random.choice(SEPS) if i + 1 != len(compiled) else ''}"
        for i, j in enumerate(compiled)
    )


@ensure_setsep
def encode(text: str, *, seeded: bool = True, tower_rows: int = 0) -> str:
    """Encode text into charabia.

    Parameters
    ----------
    text: str
        The text to encode.

    seeded: bool
        Whether each encoded character should be chose at random from the
        encoding index, or whether only the first index is ever taken. Defaults
        to randomization (True).

    tower_rows: int
        Characters per line, separated by a line break. Set to 0 to disable linewrapping
        entirely, this is done be default. When using this kwarg, output will look
        like a tower.

    Returns
    -------
    str
        The encoded text.
    """

    encoded = _encode(text, seeded)
    return create_tower(string=encoded, tower_rows=tower_rows)


@ensure_setsep
def decode(text: str) -> str:
    """Decode text from charabia.

    Paramaters
    ----------
    text: str
        The text to decode.

    Returns
    -------
    str
        The decoded text.
    """
    m = ""
    error = False

    def raise_(message="failed to decode with configuration " + SEPS):
        raise CharabiaError(message) from None

    try:
        items = ["".join(map(DECODING_INDEXES.__getitem__, s)) for s in splitseps(text)]
    except KeyError as e:
        m = "Unexpected character in token: %s" % e
        if e.args[0] == " ":
            m = "Spaces shouldn't appear inside decode(). Perhaps you meant to use encode()?"
        raise_(m)
    else:
        for i in items:
            try:
                i = int(i)
            except (OverflowError, ValueError):
                error = True
            else:
                if i not in range(1114112):
                    error = True
            finally:
                if error:
                    raise_()
                m += chr(i)
    return m


@contextlib.contextmanager
def tempseps(separators: str):
    """Temporarily alter the separator configuration with this context manager."""
    global SEPS
    original = SEPS
    setseps(separators)
    try:
        yield
    finally:
        SEPS = original


def splitseps(text: str, separators: Optional[str] = None) -> List[str]:
    """Split text from the given separators."""
    if separators is None:
        if SEPS is None:
            raise RuntimeError(
                "splitseps separator argument must not be omitted when charabia has not been configured"
            )
        separators = SEPS
    split = re.split("|".join(separators), text)
    if any(len(x) > 7 for x in split):
        # max ord: 1114111 (len(7))
        raise CharabiaError(
            "The provided charabia does not seem valid for the associated separator configuration"
        )
    return split

# Charabia

This library was designed for reversible sheltering of sensitive information/data,
meaning you can shelter strings or tokens using this encoder.

Charabia gets it's name from the French of "gibberish", as when encoded, the
text quite literally looks like a load of gibberish.

### Getting started

Import the module:

```py
import charabia
```

- `Separator Configuration`

    Firstly, you should configure the encoder to use a separator configuration. Each
    separator in the configuration has a chance to be the separator/splitter of each character
    within the encoded string.

    ```py
    charabia.setseps("ABCDEFGH")
    ```

    Alternatively, you can use a temporary configuration as a context manager by using the
    `tempsep()` method (standing for temporary separators)

    ```py
    with charabia.tempsep("ABCDEFGH"):
        ...
    ```

    Separator duplicates and insertion order is not relevant, so it does not matter what order you provide them in
    (`ABCD` == `DCBA`).

- `Separator Acknowledgement`

    The exact separator configuration is required in order to decode a specific string. This means
    it's really important to remember the separator config you used to encode a given string. 

- `Encoder`

    Now we have configured charabia, we can start encoding and decoding strings. For the following
    examples, we will use the configuration `ABCD`.

    ```py
    >>> charabia.setseps("ABCD")
    >>> codes = []
    >>> for _ in range(5):
    >>>    encoded = charabia.encode("Hello world!")
    >>>    print(encoded)
    >>>    codes.append(encoded)
    'VGBZEvCPaWBvusAvZFAnGCbFXDZlZCbPeAvkiDFukDxH'
    'VQCPYZClkWDPusAvFbCxQCvbtBPPvDFFeAbaiAbYaAHn'
    'hQAbaPAPEWCZEsDvblDdcAFPjDvbbDFleCluWBZkaCRH'
    'LwBluPBZusCFOsCPZbDHQAbPNBZvvCZFSAlOiClEuCxR'
    'hcCZOvCvEWBPOsDFvbBHwAbbjCvFFAllSCFYWBZuOBHR'
    ```

    5 unique results have been produced with this separator configuration. The longer the string,
    the more likely they are to be unique from other strings.

    Now using the same configuration, lets decode each of the strings in the `codes` list we created.

    ```py
    >>> for c in codes:
    >>>    print(charabia.decode(c))
    'Hello world!'
    'Hello world!'
    'Hello world!'
    'Hello world!'
    'Hello world!'
    ```

    Despite being different, all these results are decoded to exactly the same original string.

- `Configuration conflicts`

    Charabia operates based on the separators provided in setseps, so if the incorrect separators are
    given to decode a string, things may not work as expected.

    Let's grab one of our results from earlier, `VGBZEvCPaWBvusAvZFAnGCbFXDZlZCbPeAvkiDFukDxH`. This
    will only translate to "Hello world!" with the configuration `ABCD`, so lets change the configuration
    and see what happens:

    ```py
    >>> with charabia.tempsep("EFGH"):
    >>>     print(charabia.decode("VGBZEvCPaWBvusAvZFAnGCbFXDZlZCbPeAvkiDFukDxH"))
    CharabiaError: failed to decode with configuration EFGH
    ```
    
### Methods

- `setseps()`

    Use this function to configure the separators used for charabia. Must be alphanumeric,
    and must range between 1 and 42.

    ```py
    charabia.setseps("MySeparators123")
    ```

- `getseps()`

    Get the separators associated with the current charabia configuration.

    ```py
    >>> charabia.setseps("QwErTy103")
    >>> charabia.getseps()
    'QwErTy103'
    >>> charabia.setseps("aaaaaa")
    >>> charabia.getseps()
    'a'
    ```

- `tempseps()`

    Context manager to temporarily alter the separator configuration.
    This will fall back to the original global setting after `__exit__()`.

    ```py
    >>> with charabia.tempseps("ABC"):
    >>>     charabia.decode("ZPgCbkbCbbTCPZgCFEJAlZuCPYRARmBotBfYBfZ")
    'testing 123'
    ```

- `encode()`
    
    Use the encode method to encode standard text into charabia. Ensure that charabia is configured
    before using this method.

    ```py
    >>> charabia.setseps("AsDfGhJkL")
    >>> charabia.encode("Hello world!")
    'VwklElsPuCfFuWflFPAdwJZPNAPvlAFFIGPaMhZuOAnx'
    ```

- `decode()`

    The reverse of `encode()`. Self-explanatory, really.

    ```py
    >>> charabia.setseps("AsDfGhJkL")
    >>> charabia.decode("VwklElsPuCfFuWflFPAdwJZPNAPvlAFFIGPaMhZuOAnx")
    'Hello world!'
    ```

- `splitseps()`

    Exposed helper function used to split a string with the current or provided
    separator configuration. Seeing as this command can be used for debugging purposes,
    you can pass your own configuration straight into the command if you're not wanting
    to use tempseps for what you're trying to do. The options there :P

    ```py
    >>> charabia.setseps("fioh452")
    >>> encoded = charabia.encode("hello world!")
    >>> print(encoded)
    'bayhFEvibaCfbuW2bPb4dw5lZN5lFbfPlShZaWfFkaixn'
    >>> print(charabia.splitseps(encoded))
    ['bay', 'FEv', 'baC', 'buW', 'bPb', 'dw', 'lZN', 'lFb', 'PlS', 'ZaW', 'Fka', 'xn']
    >>> print(charabia.splitseps("VwklElsPuCfFuWflFPAdwJZPNAPvlAFFIGPaMhZuOAnx", "AsDfGhJkL"))
    ['Vw', 'lEl', 'PuC', 'FuW', 'lFP', 'dw', 'ZPN', 'Pvl', 'FFI', 'PaM', 'ZuO', 'nx']
    ```

- `create_tower()`

    The same as passing the `tower_rows` kwarg to `encode()`. Creates a tower for the given string.

    ```py
    >>> string = "bayhFEvibaCfbuW2bPb4dw5lZN5lFbfPlShZaWfFkaixn"
    >>> print(charabia.create_tower(string, 10))
    '''
    bayhFEviba
    CfbuW2bPb4
    dw5lZN5lFb
    fPlShZaWfF
    kaixn
    '''
    ```

- `demolish_tower()`

    Removes a tower from a string.

    ```py
    >>> string = """
    bayhFEviba
    CfbuW2bPb4
    dw5lZN5lFb
    fPlShZaWfF
    kaixn
    """
    >>> print(charabia.demolish_tower(string))
    'bayhFEvibaCfbuW2bPb4dw5lZN5lFbfPlShZaWfFkaixn'
    ```

### Internal exposed methods

The following methods are only designed for internal use, but are exposed for public use if wanted.

- `configured()`

    Returns whether charabia is fully configured.

- `generate_encoding_indexes()`

    Generates the encoding indexes used for a specific configuration. This is an exposed but
    internal function, so you must pass separators to it. You should only use this if you know
    what you're doing, and if you know the **encode** function well.

    ```py
    >>> print(charabia.generate_encoding_indexes("QwErTy103"))
    {
        0: ['a', 'k', 'u', 'O', 'Y'],
        1: ['b', 'l', 'v', 'F', 'P', 'Z'],
        2: ['c', 'm', 'G'],
        3: ['d', 'n', 'x', 'H', 'R'],
        4: ['e', 'o', 'I', 'S'],
        5: ['f', 'p', 'z', 'J'],
        6: ['g', 'q', 'A', 'K', 'U'],
        7: ['h', 'B', 'L', 'V'],
        8: ['i', 's', 'C', 'M', 'W'],
        9: ['j', 't', 'D', 'N', 'X']
    }
    ```

- `generate_decoding_indexes()`

    This is really just the same as the encode counterpart, use it in the same way.

    ```py
    {
        'a': '0', 'k': '0', 'u': '0', 'O': '0', 'Y': '0',
        'b': '1', 'l': '1', 'v': '1', 'F': '1', 'P': '1',
        'Z': '1', 'c': '2', 'm': '2', 'G': '2', 'd': '3',
        'n': '3', 'x': '3', 'H': '3', 'R': '3', 'e': '4',
        'o': '4', 'I': '4', 'S': '4', 'f': '5', 'p': '5',
        'z': '5', 'J': '5', 'g': '6', 'q': '6', 'A': '6',
        'K': '6', 'U': '6', 'h': '7', 'B': '7', 'L': '7',
        'V': '7', 'i': '8', 's': '8', 'C': '8', 'M': '8',
        'W': '8', 'j': '9', 't': '9', 'D': '9', 'N': '9',
        'X': '9', 'Q': ' ', 'w': ' ', 'E': ' ', 'r': ' ',
        'T': ' ', 'y': ' ', '1': ' ', '0': ' ', '3': ' ',
        '\n': ''
    }
    ```

### Installation

Install using the recommended installer, Pip.

```sh
pip install charabia
```

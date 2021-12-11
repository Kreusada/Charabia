# Charabia

Charabia - French for gibberish. Another reversible encryption based encoder.

This library was designed for reverse compatible encryption of characters,
meaning you can encrypt or shelter information using this encoder.

This library was inspired from [Ordinary](https://github.com/Kreusada/Ordinary),
a library I also wrote.

Ordinary gets it's name from the French of "gibberish", as when encoded, the
text quite literally looks like a cat sat on your keyboard.
ijkbabkbbfkeekdckhdkdckbajkbabkjhkbbakdckbagkbbhkbbfkbbgkdckbaikbafkbahkbabkdckbbgkbaekbafkbbfkeg

### Methods

- `encode()`
    
    Use the encode method to encode standard text into Charabia.

    ```py
    encode("Hello world!")
    >>> 'hckbabkbaikbaikbbbkdckbbjkbbbkbbekbaikbaakdd'
    ```

- `decode()`

    The reverse of `encode()`. Self-explanatory, really.

    ```py
    decode("hckbabkbaikbaikbbbkdckbbjkbbbkbbekbaikbaakdd")
    >>> 'Hello world!'

### Installation

Install using the recommended installer, Pip.

```sh
pip install charabia
```
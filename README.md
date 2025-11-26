# manabox-collection-scryfall-enhancer

Takes a Manabox collection export CSV, and enhances the data by fetching card details from Scryfall.

## Why?

I store my entire collection in ManaBox. For my use case, I wanted to have ChatGPT brew decks for me with only cards from my collection so I would not have to buy any new cards. I got really poor results because there was not enough data in my Manabox data export, such as a card's commander legality, color identity, and oracle text.

Now, I take my ManaBox export and run `scryfall_data_enhancer -f my-collection.csv -o enhanced-collection-data.csv`, then feed that enhanced CSV to my ChatGPT conversation and brew away!

## Running

```shell
$ scryfall_data_enhancer --help
Usage: scryfall_data_enhancer [OPTIONS]

  Command-line interface for enhancing Scryfall card data.

Options:
  -f, --input-file TEXT   Path to the input CSV file with Scryfall IDs.
                          [required]
  -o, --output-file TEXT  Path to the output CSV file for enhanced data.
                          [required]
  --help                  Show this message and exit.
$ scryfall_data_enhancer -f my-collection.csv -o enhanced-collection-data.csv
Processing card 1/5661: 665a61c9-ffdf-4e60-9a35-2176279d8b3c...
Processing card 2/5661: 79d1889c-4b3d-47d4-847e-4343cdaf9750...
...
Processing card 5661/5661: 17d71522-b133-4003-b787-0c742a2fd70e...

Processing complete!
```

## Development

1. create a python virtual environment: `python -m venv .venv`
2. activate the virtual environment: `source .venv/bin/activate`
3. install the dev requirements: `pip install -r requirements_dev.txt`
4. run the tests: `pytest`
5. build the binary: `pyinstaller --onefile scryfall_data_enhancer.py`
6. Add to your PATH: `cp dist/scryfall_data_enhancer ~/.local/bin/`

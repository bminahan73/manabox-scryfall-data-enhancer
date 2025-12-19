import os
import csv

this_dir = os.path.dirname(os.path.abspath(__file__))

def filter_cards(card_names: list[str], input_file: str, output_file: str = 'filtered_cards.csv'):
    with open(input_file, 'r') as file:
        reader = csv.DictReader(file)
        filtered_cards = [row for row in reader if row['name'] in card_names]
    with open(output_file, 'w') as file:
        writer = csv.DictWriter(file, fieldnames=reader.fieldnames)
        writer.writeheader()
        writer.writerows(filtered_cards)

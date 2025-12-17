#from ai.magic_card_selector import MagicCardSelector
from ai.magic_card_selector_light import MagicCardSelectorLight as MagicCardSelector
import pandas as pd

def split_csv_into_chunks(file_path, chunk_size=10):
    chunks = []
    for chunk in pd.read_csv(file_path, chunksize=chunk_size):
        chunks.append(chunk.fillna('').to_dict(orient='records'))
    return chunks

def filter_cards(csv_file_path, deck_concept):
    selected_cards = []
    for chunk in split_csv_into_chunks(csv_file_path):
        selector = MagicCardSelector()
        selected_cards.append(selector.select_cards(chunk, deck_concept))
    return selected_cards

if __name__ == "__main__":
    # Example usage
    csv_file_path = "test/test_data/test-collection-reduced-enhanced-expected-commander-legal.csv"
    deck_concept = "I'm building a +1/+1 counters deck"
    
    recommended_cards = filter_cards(csv_file_path, deck_concept)
    for card_set in recommended_cards:
        for card in card_set:
            print(card)

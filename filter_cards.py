#from ai.magic_card_selector import MagicCardSelector
from ai.magic_card_selector_light import MagicCardSelectorLight as MagicCardSelector
import pandas as pd

def split_csv_into_chunks(file_path, chunk_size):
    chunks = []
    for chunk in pd.read_csv(file_path, chunksize=chunk_size):
        chunks.append(chunk.fillna('').to_dict(orient='records'))
    return chunks

def filter_cards(csv_file_path, deck_concept, chunk_size, start_chunk=0):
    selected_cards = []
    chunks = split_csv_into_chunks(csv_file_path, chunk_size)
    print("number of chunks:", len(chunks))
    for i, chunk in enumerate(chunks):
        if i < start_chunk:
            continue
        print(f"Processing chunk {i+1}/{len(chunks)}")
        selector = MagicCardSelector()
        newly_selected = selector.select_cards(chunk, deck_concept)
        print(newly_selected)
        selected_cards.append(newly_selected['selected_cards'])
    return selected_cards

if __name__ == "__main__":
    csv_file_path = "test/test_data/test-collection-reduced-enhanced-expected-commander-legal.csv"
    deck_concept = "I'm building a +1/+1 counters deck"
    recommended_cards = filter_cards(csv_file_path, deck_concept, 20)
    for card_set in recommended_cards:
        for card in card_set:
            print(card)

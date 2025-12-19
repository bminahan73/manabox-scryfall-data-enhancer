from filter_cards import filter_cards

cards = filter_cards("/home/ben/magic-collection/whole-collection-reduced-enhanced-commander-legal-rw.csv", "I'm building a Boros Merry, Equire of Rohan extra combats deck with a legendary sub-theme.", chunk_size=12, start_chunk=37)
[print(card) for card in cards]
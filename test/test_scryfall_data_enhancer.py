import os
from scryfall_data_enhancer import reduce_collection_csv, enhance_card_data, filter_commander_legal, create_color_identity_csv, COLOR_IDENTITIES

this_dir = os.path.dirname(os.path.abspath(__file__))

def test_reduce_collection_csv():
    input_file = os.path.join(this_dir, 'test_data', 'test-collection.csv')
    expected_output_file = os.path.join(this_dir, 'test_data', 'test-collection-reduced-expected.csv')
    with open(expected_output_file, 'r', encoding='utf-8') as f:
        expected_content = f.read()
    actual_output_file = reduce_collection_csv(input_file)
    with open(actual_output_file, 'r', encoding='utf-8') as f:
        actual_content = f.read()
    assert expected_content == actual_content, "Reduced CSV content does not match expected output."

def test_enhance_card_data():
    input_file = os.path.join(this_dir, 'test_data', 'test-collection-reduced-expected.csv')
    expected_output_file = os.path.join(this_dir, 'test_data', 'test-collection-reduced-enhanced-expected.csv')
    with open(expected_output_file, 'r', encoding='utf-8') as f:
        expected_content = f.read()
    actual_output_file = enhance_card_data(input_file)
    with open(actual_output_file, 'r', encoding='utf-8') as f:
        actual_content = f.read()
    assert expected_content == actual_content, "Enhanced CSV content does not match expected output."

def test_filter_commander_legal():
    input_file = os.path.join(this_dir, 'test_data', 'test-collection-reduced-enhanced-expected.csv')
    expected_output_file = os.path.join(this_dir, 'test_data', 'test-collection-reduced-enhanced-commander-legal-expected.csv')
    with open(expected_output_file, 'r', encoding='utf-8') as f:
        expected_content = f.read()
    actual_output_file = filter_commander_legal(input_file)
    with open(actual_output_file, 'r', encoding='utf-8') as f:
        actual_content = f.read()
    assert expected_content == actual_content, "Commander legal CSV content does not match expected output."

def _filter_by_color_identity(color_identity, expected_file):
    input_file = os.path.join(this_dir, 'test_data', 'test-collection-reduced-enhanced-commander-legal-expected.csv')
    expected_output_file = os.path.join(this_dir, 'test_data', expected_file)
    with open(expected_output_file, 'r', encoding='utf-8') as f:
        expected_content = f.read()
    actual_output_file = create_color_identity_csv(input_file, COLOR_IDENTITIES[color_identity])
    with open(actual_output_file, 'r', encoding='utf-8') as f:
        actual_content = f.read()
    assert expected_content == actual_content, f"{color_identity} content does not match expected output."

def test_filter_by_color_identity():
    _filter_by_color_identity('colorless', 'test-collection-reduced-enhanced-commander-legal--expected.csv')
    _filter_by_color_identity('golgari', 'test-collection-reduced-enhanced-commander-legal-BG-expected.csv')
    _filter_by_color_identity('wubrg', 'test-collection-reduced-enhanced-commander-legal-WUBRG-expected.csv')

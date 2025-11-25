import os
import tempfile
from scryfall_data_enhancer import enhance_card_data
def test_scryfall_data_enhancer():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(this_dir, 'test_data', 'test-collection.csv')
    expected_output_file = os.path.join(this_dir, 'test_data', 'test-collection-enhanced.csv')
    with open(expected_output_file, 'r', encoding='utf-8') as f:
        expected_content = f.read()
    with tempfile.NamedTemporaryFile(suffix='.csv') as tmpfile:
        enhance_card_data(input_file, tmpfile.name)
        with open(tmpfile.name, 'r', encoding='utf-8') as f:
            actual_content = f.read()
    assert expected_content == actual_content, "Enhanced CSV content does not match expected output."
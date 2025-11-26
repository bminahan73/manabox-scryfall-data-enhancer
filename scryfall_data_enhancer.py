import csv
import requests
import time
import os
import click
import csv

SCRYFALL_API_USER_AGENT = "MyDeckListProcessor/1.0"

COLOR_IDENTITIES = {
    'colorless': {
        'color_identity': '',
        'legal_color_identities': ['']
    },
    'white': {
        'color_identity': 'W',
        'legal_color_identities': ['', 'W']
    },
    'blue': {
        'color_identity': 'U',
        'legal_color_identities': ['', 'U']
    },
    'black': {
        'color_identity': 'B',
        'legal_color_identities': ['', 'B']
    },
    'red': {
        'color_identity': 'R',
        'legal_color_identities': ['', 'R']
    },
    'green': {
        'color_identity': 'G',
        'legal_color_identities': ['', 'G']
    },
    'azorius': {  # White-Blue
        'color_identity': 'WU',
        'legal_color_identities': ['', 'W', 'U', 'WU']
    },
    'boros': {  # White-Red
        'color_identity': 'WR',
        'legal_color_identities': ['', 'W', 'R', 'WR']
    },
    'orzhov': {  # White-Black
        'color_identity': 'WB',
        'legal_color_identities': ['', 'W', 'B', 'WB']
    },
    'selesnya': {  # White-Green
        'color_identity': 'WG',
        'legal_color_identities': ['', 'W', 'G', 'WG']
    },
    'dimir': {  # Blue-Black
        'color_identity': 'UB',
        'legal_color_identities': ['', 'U', 'B', 'UB']
    },
    'izzet': {  # Blue-Red
        'color_identity': 'UR',
        'legal_color_identities': ['', 'U', 'R', 'UR']
    },
    'simic': {  # Blue-Green
        'color_identity': 'UG',
        'legal_color_identities': ['', 'U', 'G', 'UG']
    },
    'rakdos': {  # Black-Red
        'color_identity': 'BR',
        'legal_color_identities': ['', 'B', 'R', 'BR']
    },
    'golgari': {  # Black-Green
        'color_identity': 'BG',
        'legal_color_identities': ['', 'B', 'G', 'BG']
    },
    'gruul': {  # Red-Green
        'color_identity': 'RG',
        'legal_color_identities': ['', 'R', 'G', 'RG']
    },
    'wub': {  # White-Blue-Black
        'color_identity': 'WUB',
        'legal_color_identities': ['', 'W', 'U', 'B', 'WU', 'WB', 'UB', 'WUB']
    },
    'wur': {  # White-Blue-Red
        'color_identity': 'WUR',
        'legal_color_identities': ['', 'W', 'U', 'R', 'WU', 'WR', 'UR', 'WUR']
    },
    'wug': {  # White-Blue-Green
        'color_identity': 'WUG',
        'legal_color_identities': ['', 'W', 'U', 'G', 'WU', 'WG', 'UG', 'WUG']
    },
    'wbr': {  # White-Black-Red
        'color_identity': 'WBR',
        'legal_color_identities': ['', 'W', 'B', 'R', 'WB', 'WR', 'BR', 'WBR']
    },
    'wbg': {  # White-Black-Green
        'color_identity': 'WBG',
        'legal_color_identities': ['', 'W', 'B', 'G', 'WB', 'WG', 'BG', 'WBG']
    },
    'wrg': {  # White-Red-Green
        'color_identity': 'WRG',
        'legal_color_identities': ['', 'W', 'R', 'G', 'WR', 'WG', 'RG', 'WRG']
    },
    'ubr': {  # Blue-Black-Red
        'color_identity': 'UBR',
        'legal_color_identities': ['', 'U', 'B', 'R', 'UB', 'UR', 'BR', 'UBR']
    },
    'ubg': {  # Blue-Black-Green
        'color_identity': 'UBG',
        'legal_color_identities': ['', 'U', 'B', 'G', 'UB', 'UG', 'BG', 'UBG']
    },
    'urg': {  # Blue-Red-Green
        'color_identity': 'URG',
        'legal_color_identities': ['', 'U', 'R', 'G', 'UR', 'UG', 'RG', 'URG']
    },
    'brg': {  # Black-Red-Green
        'color_identity': 'BRG',
        'legal_color_identities': ['', 'B', 'R', 'G', 'BR', 'BG', 'RG', 'BRG']
    },
    'wubr': {  # White-Blue-Black-Red
        'color_identity': 'WUBR',
        'legal_color_identities': ['', 'W', 'U', 'B', 'R', 'WU', 'WB', 'WR', 'UB', 'UR', 'BR', 'WUB', 'WUR', 'WBR', 'UBR', 'WUBR']
    },
    'wubg': {  # White-Blue-Black-Green
        'color_identity': 'WUBG',
        'legal_color_identities': ['', 'W', 'U', 'B', 'G', 'WU', 'WB', 'WG', 'UB', 'UG', 'BG', 'WUB', 'WUG', 'WBG', 'UBG', 'WUBG']
    },
    'wurg': {  # White-Blue-Red-Green
        'color_identity': 'WURG',
        'legal_color_identities': ['', 'W', 'U', 'R', 'G', 'WU', 'WR', 'WG', 'UR', 'UG', 'RG', 'WUR', 'WUG', 'WRG', 'URG', 'WURG']
    },
    'wbrg': {  # White-Black-Red-Green
        'color_identity': 'WBRG',
        'legal_color_identities': ['', 'W', 'B', 'R', 'G', 'WB', 'WR', 'WG', 'BR', 'BG', 'RG', 'WBR', 'WBG', 'WRG', 'BRG', 'WBRG']
    },
    'ubrg': {  # Blue-Black-Red-Green
        'color_identity': 'UBRG',
        'legal_color_identities': ['', 'U', 'B', 'R', 'G', 'UB', 'UR', 'UG', 'BR', 'BG', 'RG', 'UBR', 'UBG', 'URG', 'BRG', 'UBRG']
    },
    'wubrg': {  # White-Blue-Black-Red-Green
        'color_identity': 'WUBRG',
        'legal_color_identities': ['', 'W', 'U', 'B', 'R', 'G', 'WU', 'WB', 'WR', 'WG', 'UB', 'UR', 'UG', 'BR', 'BG', 'RG', 'WUB', 'WUR', 'WBR', 'WBG', 'WRG', 'UBR', 'UBG', 'URG', 'BRG', 'WUBR', 'WUBG', 'WURG', 'WBRG', 'UBRG', 'WUBRG']
    }
}

def reduce_collection_csv(input_file) -> str:
    """
    Reduces the collection CSV to only include specific columns name and scryfall_id.
    Args:
        input_file (str): Path to the collection CSV file
    Returns:
        str: Path to the reduced CSV file
    """
    with open(input_file, mode='r', newline='', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        
        # Get the fieldnames we want to keep, with new names
        fieldnames = ['name', 'scryfall_id']
        
        # Map old names to new names
        column_mapping = {
            'Name': 'name',
            'Scryfall ID': 'scryfall_id'
        }
        
        # Filter for only the columns we want
        filtered_rows = []
        for row in reader:
            filtered_row = {}
            for old_name, new_name in column_mapping.items():
                if old_name in row:
                    filtered_row[new_name] = row[old_name]
            filtered_rows.append(filtered_row)

    output_file = input_file.replace('.csv', '-reduced.csv')

    print(f"Reducing collection CSV and saving to '{output_file}'...")

    # Write to output file
    with open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(filtered_rows)

    print("Reduction complete!")

    return output_file

def get_card_details_by_id(card_id) -> dict|None:
    """
    Fetches card details from Scryfall API using the card ID.
    Args:
        card_id (str): Scryfall card ID
    Returns:
        dict|None: Card details as returned by Scryfall API. If card is not found, returns None.
    """
    url = f"https://api.scryfall.com/cards/{card_id}"
    
    try:
        response = requests.get(
            url,
            headers={
                "Accept": "application/json",
                "User-Agent": SCRYFALL_API_USER_AGENT
            }
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred for ID '{card_id}': {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred for ID '{card_id}': {req_err}")
    except Exception as e:
        print(f"An unexpected error occurred for ID '{card_id}': {e}")

    return None

def enhance_card_data(reduced_file) -> str:
    """
    Enhances the reduced CSV file with additional card details from Scryfall API.
    Args:
        reduced_file (str): Path to the reduced CSV file
    Returns:
        str: Path to the enhanced CSV file
    """
    print(f"Reading card IDs from '{reduced_file}'...")
    with open(reduced_file, 'r', newline='', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        card_ids = [row[1] for row in reader if row and row[1] != "scryfall_id"]
    print(f"Found {len(card_ids)} card IDs to process.")
    sample_details = get_card_details_by_id(card_ids[0])
    if not sample_details:
        print("Could not fetch details for the first card to determine headers. Exiting.")
        return
    final_headers = ['name', 'scryfall_id', 'commander_legal', 'color_identity', 'mana_cost', 'cmc', 'type_line', 'power', 'toughness', 'oracle_text']
    output_file_path = reduced_file.replace('.csv', '-enhanced.csv') 
    print(f"Enhancing data and saving to '{output_file_path}'...")
    with open(output_file_path, 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(final_headers)
        for i, card_id in enumerate(card_ids):
            print(f"Processing card {i+1}/{len(card_ids)}: {card_id}...")
            details = get_card_details_by_id(card_id)
            if details:
                name = details.get('name', '')
                commander_legal = details.get('legalities', {}).get('commander', '') == 'legal'
                color_identity = ''.join(details.get('color_identity', []))
                mana_cost = details.get('mana_cost', '')
                cmc = str(int(details.get('cmc', 0)))
                type_line = details.get('type_line', '')
                power = details.get('power', '')
                toughness = details.get('toughness', '')
                oracle_text = details.get('oracle_text', '').replace('\n', ' ')
                writer.writerow([name, card_id, commander_legal, color_identity, mana_cost, cmc, type_line, power, toughness, oracle_text])
            else:
                print(f" -> Could not fetch details for {card_id}. Writing blank fields.")
                writer.writerow([card_id, '', '', '', ''])
            time.sleep(0.3) # Adjust delay as needed based on Scryfall's rate limits
    print("\nProcessing complete!")
    print(f"Enhanced data saved to '{output_file_path}'")
    return output_file_path

def filter_commander_legal(enhanced_file) -> str:
    """
    Filters the enhanced CSV file to include only commander legal cards.
    Args:
        enhanced_file (str): Path to the enhanced CSV file   
    Returns:
        str: Path to the created filtered CSV file
    """
    
    # Generate output file path based on input file name
    output_file = enhanced_file.replace('.csv', '-commander-legal.csv') 
    
    with open(enhanced_file, mode='r', newline='', encoding='utf-8') as infile, \
         open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
         
        reader = csv.DictReader(infile)
        writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
        writer.writeheader()
        
        for row in reader:
            # Check if 'commander_legal' exists and is 'True' (case-insensitive)
            if 'commander_legal' in row and row['commander_legal'].strip().lower() == 'true':
                writer.writerow(row)
    
    return output_file

def filter_by_color_identity(input_file, target_colors) -> list[dict]:
    """
    Filters rows from a CSV file that have one of the specified color identities.
    
    Args:
        input_file (str): Path to the input CSV file
        target_colors (list): List of color identity values to match
        
    Returns:
        list: List of dictionaries, where each dictionary represents a row matching the filter
    """
    matching_rows = []
    
    # Convert target colors to lowercase for case-insensitive matching
    target_colors_lower = [''.join(sorted(color.lower())) for color in target_colors]
    
    try:
        with open(input_file, mode='r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            
            for row in reader:
                # Check if 'color_identity' column exists
                if 'color_identity' in row:
                    color_identity = ''.join(sorted(row['color_identity'].strip().lower()))
                    if '' in target_colors_lower and (color_identity == '' or color_identity is None):
                        matching_rows.append(row)
                        continue
                    if color_identity in target_colors_lower:
                        matching_rows.append(row)

    except FileNotFoundError:
        print(f"Error: The file {input_file} was not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    
    return matching_rows

def create_color_identity_csv(commander_legal_file, color_identity_map: dict) -> str|None:
    """
    Filters rows from a CSV file by color identity and writes the results to a new CSV file.
    
    Args:
        commander_legal_file (str): Path to the input CSV file
        target_colors (list): List of color identity values to filter by (default: ['B', ''])
        
    Returns:
        str: Path to the output CSV file if successful, None otherwise
    """
    try:
        # Use the previously defined function to get filtered rows
        filtered_rows = filter_by_color_identity(commander_legal_file, color_identity_map['legal_color_identities'])
        
        # Generate output filename based on input file and target colors
        output_file = commander_legal_file.replace('.csv', f"-{color_identity_map['color_identity']}.csv") 

        # Write the filtered rows to the output CSV file
        with open(output_file, mode='w', newline='', encoding='utf-8') as csvfile:
            # Get headers from input file if available
            with open(commander_legal_file, mode='r', newline='', encoding='utf-8') as input_csvfile:
                reader = csv.DictReader(input_csvfile)
                fieldnames = reader.fieldnames
                
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            # Always write the header row
            writer.writeheader()
            
            # Write filtered rows if any exist
            if filtered_rows:
                writer.writerows(filtered_rows)
                
        print(f"Successfully wrote {len(filtered_rows)} rows to {output_file}")
        return output_file
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

def create_all_color_identity_csvs(commander_legal_file) -> list[str]:
    """
    Creates CSV files for all defined color identities from the commander legal cards file.
    Args:
        commander_legal_file (str): Path to the commander legal CSV file
    Returns:
        list: List of paths to the created CSV files
    """
    created_files = []
    for color_name, color_info in COLOR_IDENTITIES.items():
        print(f"Creating CSV for color identity: {color_name}...")
        output_file = create_color_identity_csv(commander_legal_file, color_info)
        if output_file:
            created_files.append(output_file)
    return created_files

@click.command()
@click.option('--collection-file', '-f', required=True, help='Path to the input CSV file with Scryfall IDs.')
def cli(collection_file):
    """
    Command-line interface to enhance card data from a collection CSV file.
    """
    reduced_file = reduce_collection_csv(collection_file)
    enhanced_file = enhance_card_data(reduced_file)
    commander_legal_file = filter_commander_legal(enhanced_file)
    create_all_color_identity_csvs(commander_legal_file)

if __name__ == "__main__":
    cli()

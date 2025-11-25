import csv
import requests
import time
import os
import click

SCRYFALL_API_USER_AGENT = "MyDeckListProcessor/1.0"

def get_card_details_by_id(card_id):
    """
    Fetches a single card's details from Scryfall using its unique ID.

    Args:
        card_id (str): The Scryfall ID of the card (e.g., 'lightning-bolt').

    Returns:
        dict: A dictionary containing the card's details if successful, None otherwise.
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
        # Scryfall uses status codes like 404 for not found, 403 for rate limits, etc.
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred for ID '{card_id}': {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred for ID '{card_id}': {req_err}")
    except Exception as e:
        print(f"An unexpected error occurred for ID '{card_id}': {e}")

    return None

def enhance_card_data(input_file_path, output_file_path):
    """
    Reads a CSV of Scryfall card IDs, fetches details for each,
    and writes an enhanced CSV file with new card details.

    Args:
        input_file_path (str): The path to the input CSV file.
    """
    print(f"Reading card IDs from '{input_file_path}'...")
    
    # Read all card IDs from the input file
    with open(input_file_path, 'r', newline='', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        card_ids = [row[8] for row in reader if row and row[8] != "Scryfall ID"] # Create a simple list of IDs
    
    print(f"Found {len(card_ids)} card IDs to process.")

    # Prepare to write the enhanced data
    # We'll use the first card to define our new headers
    sample_details = get_card_details_by_id(card_ids[0])
    
    if not sample_details:
        print("Could not fetch details for the first card to determine headers. Exiting.")
        return

    # Define the new columns we want to add
    new_headers = ['name', 'mana_cost', 'color_identity', 'type', 'oracle_text']
    
    # Prepare the full header row for our new CSV
    final_headers = ['scryfall_id'] + new_headers
    
    print(f"Enhancing data and saving to '{output_file_path}'...")
    
    with open(output_file_path, 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(final_headers)

        # Loop through each card ID, fetch details, and write the new row
        for i, card_id in enumerate(card_ids):
            print(f"Processing card {i+1}/{len(card_ids)}: {card_id}...")

            details = get_card_details_by_id(card_id)
            
            if details:
                # Extract the data for our new columns
                # Using .get() is safer as it returns None if a key doesn't exist
                name = details.get('name', '')
                mana_cost = details.get('mana_cost', '')
                color_identity = ''.join(details.get('color_identity', []))
                card_type = details.get('type_line', '')
                oracle_text = details.get('oracle_text', '').replace('\n', ' ') # Replace newlines for CSV

                # Write the new row to the output file
                writer.writerow([card_id, name, mana_cost, color_identity, card_type, oracle_text])
            else:
                # If fetching failed, write the ID but leave other fields blank
                print(f" -> Could not fetch details for {card_id}. Writing blank fields.")
                writer.writerow([card_id, '', '', '', ''])
            
            # Be a good internet citizen and respect rate limits
            time.sleep(0.1) # Scryfall allows 75 requests per second. 0.1s is safe.

    print("\nProcessing complete!")
    print(f"Enhanced data saved to '{output_file_path}'")


@click.command()
@click.option('--input-file', '-f', required=True, help='Path to the input CSV file with Scryfall IDs.')
@click.option('--output-file', '-o', required=True, help='Path to the output CSV file for enhanced data.')
def cli(input_file, output_file):
    """Command-line interface for enhancing Scryfall card data."""
    
    # Check if the input file exists before running
    if not os.path.exists(input_file):
        print(f"Error: The input file '{input_file}' was not found.")
        print("Please create this file with one Scryfall ID per row.")
    else:
        enhance_card_data(input_file, output_file)

if __name__ == "__main__":
    cli()

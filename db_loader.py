import json
import sqlite3
import ijson
import requests
from decimal import Decimal

class CustomJSONEncoder(json.JSONEncoder):
    """Custom JSON encoder that handles Decimal objects"""
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)  # Convert Decimal to float
        return super().default(obj)

SCRYFALL_API_USER_AGENT = "MyDeckListProcessor/1.0"

def update_all_cards_file(all_cards_file_path: str):
    response = requests.get('https://api.scryfall.com/bulk-data', headers={'User-Agent': SCRYFALL_API_USER_AGENT}).json()
    data_url = [data for data in response['data'] if data['type'] == 'all_cards'][0]['download_uri']
    response = requests.get(data_url, headers={'User-Agent': SCRYFALL_API_USER_AGENT})
    with open(all_cards_file_path, 'wb') as f:
        f.write(response.content)

def load_db(json_file_path: str, db_path, batch_size: int = 1000):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS json_data (
        id TEXT PRIMARY KEY,
        value TEXT
    )
    ''')
    
    insert_sql = 'INSERT OR IGNORE INTO json_data (id, value) VALUES (?, ?)'
    
    batch = []
    records_processed = 0
    
    try:
        with open(json_file_path, 'rb') as file:  # Use binary mode for ijson
            parser = ijson.items(file, 'item')
            for obj in parser:
                if 'id' not in obj:
                    raise ValueError(f"JSON object at record {records_processed + 1} must have an 'id' field")
                batch.append((obj['id'], json.dumps(obj, cls=CustomJSONEncoder)))
                records_processed += 1
                
                if len(batch) >= batch_size:
                    cursor.executemany(insert_sql, batch)
                    conn.commit()
                    batch = []
                    print(f"Processed {records_processed} records...", end='\r')
            if batch:
                cursor.executemany(insert_sql, batch)
                conn.commit()
                
        print(f"\nCompleted! Processed {records_processed} records.")
        
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

if __name__ == '__main__':
    update_all_cards_file('all_cards.json')
    load_db('all_cards.json', 'cards.db')
import json
import requests
from datetime import datetime, timedelta
import time

# Constants
BASE_URL = "https://starscape.infegy.com/api"

# Read API key from file
with open('api_key.txt', 'r') as f:
    API_KEY = f.read().strip()
AUTH_TOKEN = f"Bearer {API_KEY}"

HEADERS = {
    "accept": "application/json",
    "Authorization": AUTH_TOKEN,
    "Content-Type": "application/json",
}

def get_volume_data(query):
    """Fetch volume data for a specific query over the last month."""
    url = f"{BASE_URL}/query/agg"
    
    # Calculate date range (last 30 days)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    payload = {
        "dataset_id": "ds_gj4u3F40SLa",
        "timezone": "Etc/UTC",
        "query": query,  # Use the narrative's existing query
        "aggs": {
            "daily_volume": {
                "op": "histogram",
                "field": "published",
                "interval": "day",
                "min": start_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "max": end_date.strftime("%Y-%m-%dT%H:%M:%SZ")
            }
        }
    }

    response = requests.post(url, json=payload, headers=HEADERS)
    
    if response.status_code == 200:
        data = response.json()
        # Extract daily volumes from the histogram buckets
        try:
            volume_data = [[bucket['_key'], bucket['_count']] 
                          for bucket in data['daily_volume']['_buckets']]
            return volume_data
        except KeyError as e:
            print(f"Unexpected response structure: {e}")
            return None
    else:
        print(f"Error fetching volume data: {response.status_code}")
        return None

def update_summary_with_volume():
    """Read summary file, add volume data to each narrative, and save updated file."""
    try:
        with open('infegy_summary.json', 'r') as f:
            summary_data = json.load(f)
        
        # Process each narrative
        for narrative in summary_data['output']['narratives']:
            print(f"Fetching volume data for narrative: {narrative['title']}")
            
            # Use the narrative's existing query
            volume_data = get_volume_data(narrative['query'])
            
            if volume_data:
                # Add volume data to the narrative
                narrative['volume_data'] = volume_data
                # Add a small delay to avoid hitting rate limits
                time.sleep(1)
            else:
                print(f"Failed to fetch volume data for: {narrative['title']}")
        
        # Save updated data back to file
        with open('infegy_summary.json', 'w') as f:
            json.dump(summary_data, f, indent=2)
            
        print("Successfully updated summary file with volume data")
        
    except Exception as e:
        print(f"Error processing summary file: {str(e)}")

if __name__ == "__main__":
    update_summary_with_volume() 
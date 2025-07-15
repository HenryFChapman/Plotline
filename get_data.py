import time
import json
import requests
import urllib.parse
import os
from pushing_dataset_to_infegy_api import push_data

# Constants
BASE_URL = "https://starscape.infegy.com/api"

# Read API key from file
with open('infegy_starscape_bearer_token.txt', 'r') as f:
    API_KEY = f.read().strip()
AUTH_TOKEN = f"Bearer {API_KEY}"

HEADERS = {
    "accept": "application/json",
    "Authorization": AUTH_TOKEN,
    "Content-Type": "application/json",
}

TIMEOUT = 60
WAIT_TIME = 10  # Polling wait time
NUM_NARRATIVES = 3
DATA_DIR = "plotline_data"

def request_summary(dataset_id):
    """Requests the main structured summary and retrieves the token."""
    url = f"{BASE_URL}/query/ai-summary-structured/"
    payload = {
        "dataset_id": dataset_id,
        "query": {
            "op": "and",
            "values": [
            {
                "op": "contains",
                "field": "language",
                "value": "en"
            },
            {
                "op": "contains",
                "field": "taxonomies",
                "value": "News and Politics"
            }
            ]
        }
    }

    response = requests.post(url, json=payload, headers=HEADERS)

    if response.status_code == 200:
        data = response.json()
        token = data.get("token")
        if token:
            print(f"Successfully retrieved token: {token}")
            return token, data  # Return both token and summary data
        else:
            raise ValueError("Token not found in response.")
    else:
        raise Exception(f"Failed to retrieve summary. Status: {response.status_code}, Response: {response.text}")

def poll_async_results(token):
    """Polls the async endpoint until results are ready, with error handling."""
    url = f"{BASE_URL}/ai-async/{token}"
    start_time = time.time()

    while True:
        response = requests.get(url, headers=HEADERS)

        if response.status_code == 200:
            data = response.json()

            # Check for AI failure error
            if "error" in data and data["error"] == "The AI failed to generate valid output":
                print(f"Error: AI failed to generate valid output for token {token}")
                return {"error": "AI failed"}  # Return error marker instead of crashing

            narratives = data.get("narratives") or []

            if data.get("complete") is True or len(narratives) >= 6:
                print("Data retrieval completed successfully.")
                return data  

            elapsed_time = time.time() - start_time
            print(f"Processing... Elapsed time: {elapsed_time:.2f} seconds. Retrying in {WAIT_TIME} seconds.")
            
            if elapsed_time > TIMEOUT:
                return data
                # raise TimeoutError("Polling timed out.")

            time.sleep(WAIT_TIME)
        else:
            raise Exception(f"Failed to poll async results. Status: {response.status_code}, Response: {response.text}")

def request_personas(query):
    """Requests the social personas structured analysis and retrieves the token."""
    url = f"{BASE_URL}/query/ai-social-personas-structured/"
    
    payload = {"query": query}  # The nested query from the narrative
    
    response = requests.post(url, json=payload, headers=HEADERS)

    if response.status_code == 200:
        data = response.json()
        token = data.get("token")
        if token:
            print(f"Successfully retrieved personas token: {token}")
            return token
        else:
            raise ValueError("Personas token not found in response.")
    else:
        raise Exception(f"Failed to request personas. Status: {response.status_code}, Response: {response.text}")

def extract_persona_data(personas_data):
    """Extracts persona titles and gender distribution from the async response."""
    if "error" in personas_data:
        return [{"title": "Error: AI failed to generate output", "gender": {"m": 0, "f": 0, "n": 0}, "color": "grey"}]

    personas_list = personas_data.get("output", {}).get("personas", [])
    
    extracted_personas = []
    for persona in personas_list:
        title = persona.get("title", "Unknown Persona")
        gender = persona.get("gender", {"m": 0, "f": 0, "n": 0})
        extracted_personas.append({
            "title": title,
            "gender": gender,
            "color": determine_gender_color(gender)
        })
    
    return extracted_personas

def determine_gender_color(gender):
    """Determines color coding based on gender distribution."""
    male = gender.get("m", 0)
    female = gender.get("f", 0)

    if male > female:
        return "blue"  # More male-dominated
    elif female > male:
        return "pink"  # More female-dominated
    else:
        return "grey"  # Neutral/mixed

def enrich_narratives_with_personas(narratives):
    """Fetches personas for the top narratives and adds them to the data."""
    for narrative in narratives:
        query = narrative.get("query")
        if not query:
            print("Skipping narrative (no query found).")
            continue

        try:
            personas_token = request_personas(query)
            personas_data = poll_async_results(personas_token)

            # Extract persona titles + gender data and add them to the narrative
            narrative["personas"] = extract_persona_data(personas_data)
        
        except Exception as e:
            narrative["personas"] = [{"title": "Error fetching personas", "gender": {"m": 0, "f": 0, "n": 0}, "color": "grey"}]

    return narratives

def request_nested_narratives(query, dataset_id):
    """Requests nested narratives analysis for a specific narrative query."""
    url = f"{BASE_URL}/query/ai-summary-structured/"
    
    payload = {
        "query": query,
        "dataset_id": dataset_id
    }  # Use the narrative's existing query
    
    response = requests.post(url, json=payload, headers=HEADERS)

    if response.status_code == 200:
        data = response.json()
        token = data.get("token")
        if token:
            print(f"Successfully retrieved nested narratives token: {token}")
            return token
        else:
            raise ValueError("Nested narratives token not found in response.")
    else:
        raise Exception(f"Failed to request nested narratives. Status: {response.status_code}, Response: {response.text}")

def enrich_narratives_with_nested_data(narratives, dataset_id):
    """Fetches nested narrative analysis for each narrative."""
    for narrative in narratives:
        print(f"\nProcessing nested narratives for: {narrative['title']}")

        query = narrative.get("query")
        if not query:
            print("Skipping narrative (no query found).")
            continue

        try:
            # Get nested narratives
            nested_token = request_nested_narratives(query, dataset_id)
            nested_data = poll_async_results(nested_token)

            if "error" in nested_data:
                print(f"Error getting nested narratives for {narrative['title']}")
                narrative["nested_narratives"] = []
                continue

            # Extract and add nested narratives to the parent narrative
            nested_narratives = nested_data.get("output", {}).get("narratives", [])
            print(f"Found {len(nested_narratives)} nested narratives")
            
            # Add the nested narratives to the parent narrative
            narrative["nested_narratives"] = nested_narratives

            # Add a small delay to avoid rate limiting
            time.sleep(1)
        
        except Exception as e:
            print(f"Error processing nested narratives for {narrative['title']}: {e}")
            narrative["nested_narratives"] = []

    return narratives

def save_result(data, dataset_name):
    """Saves the result to a JSON file."""

    filename = f"{DATA_DIR}/{dataset_name}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    print(f"Results saved to {filename}")

def get_starscape_dataset_id():

    query = '[{"id":"_user","op":"contains","value":"Henry.chapman"}]'

    params = {
        "schema": 1,
        "per_page": 1,
        "page": 1,
        "minimal": 1,
        "admin": 1,
        "q": query
    }

    encoded_params = urllib.parse.urlencode(params)

    url = f"{BASE_URL}/obj/dataset?{encoded_params}"

    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()

    return response.json()['output'][0]['id']

def generate_manifest():
    manifest = []
    for filename in os.listdir(DATA_DIR):
        if filename.endswith(".json"):
            manifest.append({
                "file": os.path.join(DATA_DIR, filename),
                "label": os.path.splitext(filename)[0]
            })
    with open("data_manifest.json", "w") as f:
        json.dump(manifest, f, indent=4)

def main():
    
    dataset_name = "MKBHD Comments"
    
    print("Uploading Data...")
    push_data(dataset_name)
    print("Finished Uploading Data.")

    dataset_id = get_starscape_dataset_id()
    print("Infegy Dataset ID: ", dataset_id)

    # Step 1: Get the main summary
    token, summary_data = request_summary(dataset_id)
    result_data = poll_async_results(token)

    # Step 2: Extract narratives
    narratives = result_data.get("output", {}).get("narratives", [])[:NUM_NARRATIVES]

    try:
        if narratives:
            # Step 3: Enrich with nested narratives
            print("\nEnriching narratives with nested data...")
            enriched_with_nested = enrich_narratives_with_nested_data(narratives, dataset_id)
            
            # Step 4: Enrich with personas
            print("\nEnriching narratives with personas data...")
            fully_enriched_narratives = enrich_narratives_with_personas(enriched_with_nested)
            
            result_data["output"]["narratives"] = fully_enriched_narratives

        # Step 5: Add overall sentiment, total count, and timestamps to JSON
        result_data["output"]["total_count"] = summary_data.get("total_count")
        result_data["output"]["positivity"] = summary_data.get("positivity")
        result_data["output"]["min_timestamp"] = summary_data.get("min_timestamp")
        result_data["output"]["max_timestamp"] = summary_data.get("max_timestamp")

        # Step 6: Save final JSON
        save_result(result_data, dataset_name)
        print("\nSuccessfully saved enriched data to JSON file")

    except Exception as e:
        print(f"Error: {e}")

    generate_manifest()

if __name__ == "__main__":
    main()

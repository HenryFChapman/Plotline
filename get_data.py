import time
import json
import requests
from get_volume_data import get_volume_data
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

TIMEOUT = 10 * 60  # 10 minutes in seconds
WAIT_TIME = 10  # Polling wait time
OUTPUT_FILE = "infegy_summary_3.json"

def request_summary():
    """Requests the main structured summary and retrieves the token."""
    url = f"{BASE_URL}/query/ai-summary-structured/"
    payload = {
        "query": {
            "op": "and",
            "values": [
                {
                    "op": ">",
                    "value": "-P21D",
                    "field": "published"
                },
                {
                    "op": "contains",
                    "field": "taxonomies",
                    "value": "News and Politics"
                },
                {
                    "op": "contains",
                    "field": "language",
                    "value": "en"
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

            if data.get("complete") == True:
                print("Data retrieval completed successfully.")
                return data  

            elapsed_time = time.time() - start_time
            print(f"Processing... Elapsed time: {elapsed_time:.2f} seconds. Retrying in {WAIT_TIME} seconds.")
            
            if elapsed_time > TIMEOUT:
                raise TimeoutError("Polling timed out after 10 minutes.")

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
        return [{"title": "Error: AI failed to generate output", "gender": {"m": 0, "f": 0, "n": 0}, "color": "gray"}]

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
        return "purple"  # Neutral/mixed

def enrich_narratives_with_personas(narratives):
    """Fetches personas for the top 5 narratives and adds them to the data."""
    for narrative in narratives:
        print(f"Processing personas for narrative: {narrative['title']}")

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
            print(f"Error processing personas for {narrative['title']}: {e}")
            narrative["personas"] = [{"title": "Error fetching personas", "gender": {"m": 0, "f": 0, "n": 0}, "color": "gray"}]

    return narratives

def request_nested_narratives(query):
    """Requests nested narratives analysis for a specific narrative query."""
    url = f"{BASE_URL}/query/ai-summary-structured/"
    
    payload = {"query": query}  # Use the narrative's existing query
    
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

def enrich_narratives_with_nested_data(narratives):
    """Fetches nested narrative analysis for each narrative."""
    for narrative in narratives:
        print(f"\nProcessing nested narratives for: {narrative['title']}")

        query = narrative.get("query")
        if not query:
            print("Skipping narrative (no query found).")
            continue

        try:
            # Get nested narratives
            nested_token = request_nested_narratives(query)
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

def save_result(data, filename=OUTPUT_FILE):
    """Saves the result to a JSON file."""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    print(f"Results saved to {filename}")

def main():

    # Step 1: Get the main summary
    token, summary_data = request_summary()
    result_data = poll_async_results(token)

    # Step 2: Extract narratives
    narratives = result_data.get("output", {}).get("narratives", [])[:5]

    try:
        if narratives:
            # Step 3: Enrich with nested narratives
            print("\nEnriching narratives with nested data...")
            enriched_with_nested = enrich_narratives_with_nested_data(narratives)
            
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
        save_result(result_data)
        print("\nSuccessfully saved enriched data to JSON file")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

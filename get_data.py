import time, json, requests, urllib.parse, os
from pushing_dataset_to_infegy_api import push_data
from simulate_run import simulate

BASE_URL = "https://starscape.infegy.com/api"
DATA_DIR = "plotline_data"
TIMEOUT, WAIT_TIME, NUM_NARRATIVES = 60, 10, 4

# Read API key
with open('infegy_starscape_bearer_token.txt') as f:
    AUTH_TOKEN = f"Bearer {f.read().strip()}"

HEADERS = {
    "accept": "application/json",
    "Authorization": AUTH_TOKEN,
    "Content-Type": "application/json",
}

def post_request(endpoint, payload):
    url = f"{BASE_URL}{endpoint}"
    response = requests.post(url, json=payload, headers=HEADERS)
    response.raise_for_status()
    token = response.json().get("token")
    if not token:
        raise ValueError(f"Token not found for endpoint {endpoint}")
    print(f"Token retrieved: {token}")
    return token, response.json()

def poll_token(token):
    url = f"{BASE_URL}/ai-async/{token}"
    start = time.time()
    while True:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        data = response.json()

        if "error" in data:
            print(f"AI failed for token {token}")
            return {"error": "AI failed"}

        if data.get("complete") or len(data.get("narratives", [])) >= 6:
            return data

        if time.time() - start > TIMEOUT:
            return data  # fallback: return best effort

        time.sleep(WAIT_TIME)

def determine_gender_color(gender):
    return "blue" if gender["m"] > gender["f"] else "pink" if gender["f"] > gender["m"] else "grey"

def extract_personas(data):
    if "error" in data:
        return [{"title": "AI Failed", "gender": {"m": 0, "f": 0, "n": 0}, "color": "grey"}]
    return [{
        "title": p.get("title", "Unknown"),
        "gender": p.get("gender", {}),
        "color": determine_gender_color(p.get("gender", {}))
    } for p in data.get("output", {}).get("personas", [])]

def enrich_with_personas(narratives):
    for n in narratives:
        query = n.get("query")
        if not query: continue
        try:
            token, _ = post_request("/query/ai-social-personas-structured/", {"query": query})
            personas_data = poll_token(token)
            n["personas"] = extract_personas(personas_data)
        except Exception:
            n["personas"] = [{"title": "Error", "gender": {"m": 0, "f": 0, "n": 0}, "color": "grey"}]
    return narratives

def enrich_with_nested(narratives, dataset_id):
    for n in narratives:
        query = n.get("query")
        if not query: continue
        try:
            payload = {"query": query, "dataset_id": dataset_id}
            token, _ = post_request("/query/ai-summary-structured/", payload)
            nested_data = poll_token(token)
            n["nested_narratives"] = nested_data.get("output", {}).get("narratives", [])
            time.sleep(1)
        except Exception:
            n["nested_narratives"] = []
    return narratives

def get_dataset_id():
    query = urllib.parse.urlencode({
        "schema": 1, "per_page": 1, "page": 1, "minimal": 1,
        "admin": 1, "q": '[{"id":"_user","op":"contains","value":"Henry.chapman"}]'
    })
    url = f"{BASE_URL}/obj/dataset?{query}"
    response = requests.get(url, headers=HEADERS)
    return response.json()["output"][0]["id"]

def save_result(data, name):
    path = f"{DATA_DIR}/{name}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    print(f"Saved: {path}")

def generate_manifest():
    manifest = [{"file": os.path.join(DATA_DIR, f), "label": f.split(".")[0]}
                for f in os.listdir(DATA_DIR) if f.endswith(".json")]
    with open("data_manifest.json", "w") as f:
        json.dump(manifest, f, indent=4)

def run(dataset_id, name, upload_data):

    if upload_data.lower() == "yes":
        print("Uploading...")
        push_data(name)
        dataset_id = dataset_id or get_dataset_id()
        print(dataset_id)

    # Step 1: Main summary
    token, summary_meta = post_request("/query/ai-summary-structured/", {
        "dataset_id": dataset_id,
        "query": {
  "op": "and",
  "values": [
    {
      "op": "contains",
      "fields": [
        "title",
        "description",
        "body"
      ],
      "values": [
        "server"
      ],
      "labels": [
        "server"
      ]
    },
    {
      "op": "contains",
      "fields": [
        "title",
        "description",
        "body"
      ],
      "values": [
        "monitoring"
      ],
      "labels": [
        "monitoring"
      ]
    },
    {
      "op": "range",
      "field": "published",
      "lower": "-P3Y",
      "upper": "now"
    }
  ]
}
    })

    result = poll_token(token)
    narratives = result.get("output", {}).get("narratives", [])[:NUM_NARRATIVES]

    if narratives:
        narratives = enrich_with_nested(narratives, dataset_id)
        narratives = enrich_with_personas(narratives)
        result["output"]["narratives"] = narratives

    for k in ["total_count", "positivity", "min_timestamp", "max_timestamp"]:
        result["output"][k] = summary_meta.get(k)

    save_result(result, name)
    generate_manifest()

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--dataset_id", type=str)
    p.add_argument("--simulate", type=str, required=True)
    p.add_argument("--dataset_name", required=True)
    p.add_argument("--upload_data", type=str, required=True)
    args = p.parse_args()

    if args.simulate.lower() == "yes":
        simulate(args.dataset_id, args.dataset_name, args.upload_data)
        generate_manifest()
    else:
        run(args.dataset_id, args.dataset_name, args.upload_data)

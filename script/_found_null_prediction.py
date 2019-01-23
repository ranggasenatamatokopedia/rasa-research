import json
from sklearn.metrics import classification_report

rasa_json_format = {
    "rasa_nlu_data": {
        "common_examples": [],
        "regex_features": [],
        "lookup_tables": [],
        "entity_synonyms": []
    }
}

def analys_json_data(directory):
    count = 0
    with open(directory, 'r') as f:
        json_data = json.load(f)
        for obj in json_data:
            if obj["prediction"] == "":
                count += 1
                rasa_json_format["rasa_nlu_data"]["common_examples"].append({"text": obj["text"],
                                                                                "intent": obj["actual"]})
    # print(count)
    return rasa_json_format



if __name__ == "__main__":
    directory = "json/dialogflow_result_distinct_tambahan.json"
    rasa_json = analys_json_data(directory)
    print(json.dumps(rasa_json, sort_keys=True, indent=4))


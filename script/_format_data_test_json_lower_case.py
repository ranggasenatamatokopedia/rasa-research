#!/usr/bin/python -tt
import json


def generate_json(selected_json):
    rasa_json_format = {
        "rasa_nlu_data": {
            "common_examples": [],
            "regex_features": [],
            "lookup_tables": [],
            "entity_synonyms": []
        }
    }
    try:
        with open(selected_json, 'r') as f:
            json_data = json.load(f)
            for obj in json_data["rasa_nlu_data"]["common_examples"]:
                rasa_json_format["rasa_nlu_data"]["common_examples"].append({"text": obj["text"],
                                                                             "intent": obj["intent"].lower()})
    except OSError as e:
        print("error")
    return rasa_json_format


def convert_df_to_rasa_standard(directory):
    rasa_json = generate_json(directory)
    # print(json.dumps(rasa_json, sort_keys=True, indent=4))


def main():
    # Diretory export file dialogflow
    directory = "json/data_test.json"
    # -----------------------------------------------------#
    # Begin convert json flow to rasa standard json'
    convert_df_to_rasa_standard(directory)


if __name__ == "__main__":
    main()

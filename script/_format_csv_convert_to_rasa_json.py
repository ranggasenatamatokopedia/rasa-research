import csv
import json


def csv_file_reader(directory):
    with open(directory) as f:
        rasa_json_format = {
            "rasa_nlu_data": {
                "common_examples": [],
                "regex_features": [],
                "lookup_tables": [],
                "entity_synonyms": []
            }
        }
        reader = csv.DictReader(f)  # read rows into a dictionary format
        for row in reader:  # read a row as {column1: value1, column2: value2,...}
            desired = ""
            text = ""
            for (k, v) in row.items():  # go over each column name and value
                if k == "User Says":  # text
                    text = v.lower()
                if k == "Intent Name":  # desired intent
                    desired = v.lower()
            rasa_json_format["rasa_nlu_data"]["common_examples"].append({"text": text,
                                                                         "intent": desired})
        return rasa_json_format


if __name__ == "__main__":
    direct = "csv/w2v_generate_n_from_original.csv"
    data = csv_file_reader(direct)
    print(json.dumps(data, sort_keys=True, indent=4))

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
                if k == "text":  # text
                    text = v.lower()
                if k == "Intent":  # desired intent
                    desired = v.lower()
            rasa_json_format["rasa_nlu_data"]["common_examples"].append({"text": text,
                                                                         "intent": desired})
        return rasa_json_format


if __name__ == "__main__":
    direct = "csv/[Talk_Discussion Chatbot] DF vs Abhinav - testing_data (1).csv"
    data = csv_file_reader(direct)
    print(json.dumps(data, sort_keys=True, indent=4))

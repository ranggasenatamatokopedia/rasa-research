import csv
import json

def csv_file_reader_intent(directory):
    with open(directory) as f:
        data = []
        reader = csv.DictReader(f)  # read rows into a dictionary format
        for row in reader:  # read a row as {column1: value1, column2: value2,...}
            for (k, v) in row.items():  # go over each column name and value
                if k == "intent_name":  # text
                    text = v.lower()
                    data.append(text)
        return data

def csv_file_reader_text(directory, data):
    with open(directory) as f:
        rasa_json_format = {
            "rasa_nlu_data": {
                "common_examples": [],
                "regex_features": [],
                "lookup_tables": [],
                "entity_synonyms": []
            }
        }
        counter = 1
        index = 0
        text = ""
        reader = csv.DictReader(f)  # read rows into a dictionary format
        for row in reader:  # read a row as {column1: value1, column2: value2,...}
            for (k, v) in row.items():  # go over each column name and value
                if k == "original" and text != v.lower():  # text
                    text = v.lower()
                    rasa_json_format["rasa_nlu_data"]["common_examples"].append({"text": text,
                                                                                 "intent": data[index]})
                if k == "generated":  # text
                    generated = v.lower()
                    rasa_json_format["rasa_nlu_data"]["common_examples"].append({"text": generated,
                                                                                 "intent": data[index]})
            if(counter % 2 == 0):
                index += 1
            counter += 1
        return rasa_json_format

if __name__ == "__main__":
    direct = "csv/training_data.csv"
    data = csv_file_reader_intent(direct)
    direct = "csv/w2v_generate_n_from_original.csv"
    data = csv_file_reader_text(direct, data)
    print(json.dumps(data, sort_keys=True, indent=4))


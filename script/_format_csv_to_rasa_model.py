import csv
import re
import json

def remove_size(text):
    return re.sub("size ","",text)

def csv_file_reader(directory):
    text = {}
    data = []
    with open(directory) as f:
        reader = csv.DictReader(f)
        for row in reader:
            index = ""
            word = ""
            for (k, v) in row.items():
                if k == "Group":
                    if index != word:
                        try:
                            text[remove_size(index)].append(remove_size(word))
                        except:
                            text[remove_size(index)] = []
                            text[remove_size(index)].append(remove_size(word))
                    if v == "size":
                        size_word = word.split(" ")[0]
                        try:
                            if size_word not in text["size"]:
                                text["size"].append(size_word)
                        except:
                            text["size"] = []
                            if size_word not in text["size"]:
                                text["size"].append(size_word)
                if k == "Word":
                    index = v.lower()
                if k == "Typo":
                    word = v.lower()
                if k == "":
                    v = re.sub('"*',"",v)
                    data.append(v.split(","))
    return text, data

def rasa_model(text, data):
    rasa_json_format = {
        "rasa_nlu_data": {
            "common_examples": [],
            "regex_features": [],
            "lookup_tables": [],
            "entity_synonyms": []
        }
    }
    for value in text:
        rasa_json_format["rasa_nlu_data"]["entity_synonyms"].append({"value": value,
                                                                     "synonyms": [synm for synm in text[value]]})
    for array_setence in data:
        for setence in array_setence:
            rasa_json_format["rasa_nlu_data"]["common_examples"].append({"text": setence,
                                                                         "intent": "ready_kosong_question"})

    return rasa_json_format


if __name__ == "__main__":
    direct = "csv/string.csv"
    text, data = csv_file_reader(direct)
    rasa = rasa_model(text, data)
    # # print(rasa)
    print(json.dumps(rasa, sort_keys=True, indent=4))

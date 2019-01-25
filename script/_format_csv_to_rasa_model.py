import csv
import re
import json

def csv_file_reader(directory):
    text = {}
    data = []
    entities = {}
    with open(directory) as f:
        reader = csv.DictReader(f)
        for row in reader:
            index = ""
            word = ""
            for (k, v) in row.items():
                if k == "Group":
                    try:
                        entities[v].append(word)
                    except:
                        entities[v] = []
                        entities[v].append(word)
                    if v == "size":
                        size_word = word.split(" ")[1]
                        if index != word:
                            size_index = index.split(" ")[1]
                            try:
                                text["size "+size_index].append(word)
                            except:
                                text["size "+size_index] = []
                                text["size "+size_index].append(word)
                            continue
                        try:
                            text["size "+size_word].append(word)
                        except:
                            text["size "+size_word] = []
                            text["size "+size_word].append(word)
                    else:
                        if index != word:
                            try:
                                text[index].append(word)
                            except:
                                text[index] = []
                                text[index].append(word)
                if k == "Word":
                    index = v.lower()
                if k == "Typo":
                    word = v.lower()
                if k == "":
                    v = re.sub('"*',"",v)
                    data.append(v.split(","))
    return text, data, entities

def rasa_model(text, data, entities):
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
            data_entity = []
            start = 0
            for entity in entities:
                for word in entities[entity]:
                    try:
                        start_index = re.search(word, setence[start:]).start()
                        actual_value = word
                        for value in text:
                            if word == value:
                                actual_value = value
                                break
                            else:
                                for synm in text[value]:
                                    if word == synm:
                                        actual_value = value
                                        break
                            if actual_value != word:
                                break
                        data_entity.append({
                            "start": start_index,
                            "end": start_index+len(word),
                            "value": actual_value,
                            "entity": entity
                        })
                        start = start_index+len(word)
                    except:
                        continue
            if len(data_entity) > 0:
                rasa_json_format["rasa_nlu_data"]["common_examples"].append({"text": setence,
                                                                         "intent": "ready_kosong_question",
                                                                            "entities": data_entity})
            else:
                rasa_json_format["rasa_nlu_data"]["common_examples"].append({"text": setence,
                                                                             "intent": "ready_kosong_question"})

    return rasa_json_format


if __name__ == "__main__":
    direct = "csv/string.csv"
    text, data, entities = csv_file_reader(direct)
    for entity in entities:
        entities[entity].sort(key=len, reverse= True)
    # print(entities)
    rasa = rasa_model(text, data, entities)
    # print(rasa)
    print(json.dumps(rasa, sort_keys=True, indent=4))

import csv
import re
import json

def csv_file_reader_variant(directory):
    text = {}
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
    return text, entities

def csv_file_reader_text(directory):
    data = []
    with open(directory, 'r', newline='', encoding='ISO-8859-1') as f:
        reader = csv.DictReader(f)
        for row in reader:
            for (k, v) in row.items():
                if k == "Text":
                    data.append(v)
    return data

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
    for setence in data:
        # setence = "warna 2biru ukuran 40 ada ga sis "
        data_entity = []
        # print(entities)
        kalimat = setence
        for entity in entities:
            # print(entities[entity])
            entities[entity].sort(key=len, reverse=True)
            # print(entities[entity])
            for word in entities[entity]:
                try:
                    # print(kalimat)
                    # print(word)
                    start_index = re.search(word, kalimat).start()
                    start_index = re.search(word, setence).start()
                    kalimat = kalimat.replace(word,'')
                    # print(setence)
                    # print(start_index)
                    actual_value = word
                    for value in text:
                        if word in value:
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
                except:
                    continue
        # print(data_entity)
        if len(data_entity) > 0:
            rasa_json_format["rasa_nlu_data"]["common_examples"].append({"text": setence,
                                                                        "intent": "ready_kosong_question",
                                                                        "entities": data_entity})
        else:
            rasa_json_format["rasa_nlu_data"]["common_examples"].append({"text": setence,
                                                                         "intent": "ready_kosong_question",
                                                                         "entitites": []})

    return rasa_json_format


if __name__ == "__main__":
    direct = "csv/string.csv"
    direct_text = "csv/text_variant.csv"
    text, entities = csv_file_reader_variant(direct)
    for entity in entities:
        entities[entity].sort(key=len, reverse= True)
    data = csv_file_reader_text(direct_text)
    # print(data)
    # print(entities)
    rasa = rasa_model(text, data, entities)
    # print(rasa)
    print(json.dumps(rasa, sort_keys=True, indent=4))

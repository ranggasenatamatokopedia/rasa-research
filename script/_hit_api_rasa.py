import requests
import json

url = 'http://172.31.14.26:5000/parse'

def read_json_data(directory):
    data = []
    with open(directory, 'r') as f:
        json_data = json.load(f)
        for obj in json_data:
            for new_obj in json_data[obj]["common_examples"]:
                data.append({"intent_name": new_obj["intent"],
                            "user_says": new_obj["text"]})
    return data

def hit_api(json):
    array_obj = []
    counter = 1
    len_data = len(json)
    for test_data in json:
        print(str(counter)+ "/"+ str(len_data))
        data = {
            'q' : test_data["user_says"],
            'project' : 'rangga'
        }
        print("text : "+test_data["user_says"])
        print("actual : "+test_data["intent_name"])
        resp = requests.post(url=url, json=data)
        json = resp.json()
        print(json)
        if json["intent"]["confidence"] < 0.5:
            array_obj.append({"text": test_data["user_says"],
                              "actual": test_data["intent_name"],
                              "prediction": "default fallback intent",
                              "confidence": json["intent"]["confidence"],
                              "suggestion": json["intent_ranking"],
                              "entities": json["entities"]})
            print("predict : default fallback intent")
        else:
            array_obj.append({"text": test_data["user_says"],
                              "actual": test_data["intent_name"],
                              "prediction": json["intent"]["name"],
                              "confidence": json["intent"]["confidence"],
                              "suggestion": json["intent_ranking"],
                              "entities": json["entities"]})
            print("predict : "+json["intent"]["name"])
        counter += 1
    return array_obj

def write_json(data):
    with open('output/rasa_result_variant.json', 'w') as outfile:
        json.dump(data, outfile, sort_keys=False, indent=4)

if __name__ == "__main__":
    directory_json = "json/test_variant.json"
    data = read_json_data(directory_json)
    data = hit_api(data)
    write_json(data)

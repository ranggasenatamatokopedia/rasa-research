import json
import csv
from sklearn.metrics import classification_report


def read_json_data(directory):
    data = []
    with open(directory, 'r') as f:
        json_data = json.load(f)
        for obj in json_data:
            for new_obj in json_data[obj]["common_examples"]:
                data.append({"intent_name": new_obj["intent"],
                            "user_says": new_obj["text"]})
    return data

def write_csv(data):
    with open('output/training_data.csv', 'w') as csvFile:
        fields = ['intent_name', 'user_says']
        writer = csv.DictWriter(csvFile, fieldnames=fields)
        writer.writeheader()
        writer.writerows(data)
        print("writing completed")
        csvFile.close()


if __name__ == "__main__":
    directory_json = "json/training_data.json"
    data = read_json_data(directory_json)
    write_csv(data)
    # print(classification_report(y_true, y_pred))

import json
import csv
from sklearn.metrics import classification_report


def read_json_data(directory):
    data = []
    with open(directory, 'r') as f:
        json_data = json.load(f)
        for obj in json_data:
            if len(obj['entities']):
                variant = []
                for entity in obj['entities']:
                    variant.append(entity['entity'] + ': ' + entity['value'])
                data.append({'Text': obj['text'], 'Actual': obj['actual'], 'Predict': obj['prediction'], 'Score': obj['confidence'], 'Variant': variant})
            else:
                data.append({'Text': obj['text'], 'Actual': obj['actual'], 'Predict': obj['prediction'], 'Score': obj['confidence'], 'Variant': []})

    return data

def write_csv(data):
    with open('output/rasa_result_variant.csv', 'w') as csvFile:
        fields = ['Text', 'Actual', 'Predict', 'Score', 'Variant']
        writer = csv.DictWriter(csvFile, fieldnames=fields)
        writer.writeheader()
        writer.writerows(data)
        print("writing completed")
        csvFile.close()


if __name__ == "__main__":
    directory_json = "output/rasa_result_variant.json"
    data = read_json_data(directory_json)
    write_csv(data)
    # print(classification_report(y_true, y_pred))

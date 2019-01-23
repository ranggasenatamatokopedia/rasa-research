import json
from sklearn.metrics import classification_report

y_true = []
y_pred = []

def analys_json_data(directory):
    counter = 0
    with open(directory, 'r') as f:
        json_data = json.load(f)
        for obj in json_data:
            y_true.append(obj["actual"].lower())
            y_pred.append(obj["prediction"].lower())
    print(counter)


if __name__ == "__main__":
    directory = "output/rasa_result_distinct.json"
    analys_json_data(directory)
    print(classification_report(y_true, y_pred))
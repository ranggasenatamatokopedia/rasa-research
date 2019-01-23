import json
import csv
from sklearn.metrics import classification_report


def read_json_data(directory):
    data = []
    with open(directory, 'r') as f:
        json_data = json.load(f)
        for obj in json_data:
            prediction = []
            for suggestion in obj["suggestion"]:
                prediction.append(suggestion["name"] + "[Score: " + str(suggestion["confidence"])+"]")
            data.append({"dialogflow": obj["actual"],
                         "rasa": obj["prediction"],
                         "score" : obj["confidence"],
                         "suggestion": ", ".join(prediction),
                         "text": obj["text"]})
    return data


# def read_csv_data(data, directory):
#     with open(directory) as f:
#         counter = 0
#         reader = csv.DictReader(f)  # read rows into a dictionary format
#         for row in reader:  # read a row as {column1: value1, column2: value2,...}
#             for (k, v) in row.items():  # go over each column name and value
#                 if k == "Main Predict":  # desired intent
#                     true_data = v.lower()
#                     data[counter]['dialogflow'] = true_data
#                     counter += 1
#     return data


def write_csv(data):
    with open('output/rasa_test_report_10.csv', 'w') as csvFile:
        fields = ['dialogflow', 'rasa', 'score', "suggestion", "text"]
        writer = csv.DictWriter(csvFile, fieldnames=fields)
        writer.writeheader()
        writer.writerows(data)
        print("writing completed")
        csvFile.close()


if __name__ == "__main__":
    directory_json = "json/rasa_parse_logistik_10.json"
    data = read_json_data(directory_json)
    directory_csv = "csv/df_parse.csv"
    # data = read_csv_data(data, directory_csv)
    write_csv(data)
    # print(classification_report(y_true, y_pred))

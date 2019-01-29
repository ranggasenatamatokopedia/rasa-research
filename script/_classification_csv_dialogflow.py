import csv
from sklearn.metrics import classification_report

y_pred = []
y_true = []

counter = 0  # count total data
false = 0  # true intent
true = 0  # false intentfalse = 0  # true intent

with open('output/rasa_result_variant_10k.csv') as f:
    reader = csv.DictReader(f)  # read rows into a dictionary format
    for row in reader:  # read a row as {column1: value1, column2: value2,...}
        dialog_flow = ""
        true_data = ""

        counter = counter + 1
        for (k, v) in row.items():  # go over each column name and value
            if k == "Actual":  # desired intent
                true_data = v.lower()
                y_true.append(true_data)
            if k == "Predict":  # dialogflow
                if v == "not_ready_kosong_question":
                    dialog_flow = "default fallback intent"
                else:
                    dialog_flow = v.lower()
                y_pred.append(dialog_flow)

        if true_data != dialog_flow:
            false = false + 1
        else:
            true = true + 1

print(classification_report(y_true, y_pred))
print("True ", true)
print("False ", false)
print("Total Data ", counter)

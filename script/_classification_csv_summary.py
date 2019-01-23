import csv
from sklearn.metrics import classification_report

y_true = []
y_pred_df= []
y_pred_rasa= []
y_pred_rasa_suggest = []

def analysis_df_rasa_and_suggest(directory):
    with open(directory) as f:
        reader = csv.DictReader(f)  # read rows into a dictionary format
        for row in reader:  # read a row as {column1: value1, column2: value2,...}
            predict = 0
            for (k, v) in row.items():  # go over each column name and value
                if k == "actual":  # desired intent
                    true_data = v.lower()
                    y_true.append(true_data)
                if k == "dialogflow":  # dialogflow
                    predict = v.lower()
                    y_pred_df.append(predict)
                if k == "rasa":  # suggestion
                    predict = v.lower()
                    y_pred_rasa.append(predict)
                    y_pred_rasa_suggest.append(predict)
                    predict = 1
                if k == "suggestion" and not predict:  # suggestion
                    predict = v.split(", ").lower()
                    for suggest in predict:
                        print(true_data)
                        y_pred_rasa_suggest.append(predict)


if __name__ == "__main__":
    directory = "output/rasa_test_report.csv"
    analysis_df_rasa_and_suggest(directory)
    print("#-----------------------DIALOG FLOW---------------------------#")
    print(classification_report(y_true, y_pred_df))
    print("#-----------------------Rasa Predict--------------------------#")
    print(classification_report(y_true, y_pred_rasa))
    print("#-----------------------Rasa Suggest--------------------------#")
    print(classification_report(y_true, y_pred_rasa_suggest))
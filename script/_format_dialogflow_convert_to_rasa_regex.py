#!/usr/bin/python -tt
import os
import json
import sys, getopt
import re


counter = 0

def parent_id_not_exist(src):
    with open(src, 'r') as f:
        json_data = json.load(f)
        if "parentId" not in json_data:
            return True
        return False


def select_json_file(directory):
    selected_json = []
    for filename in os.listdir(directory):
        if filename.endswith("_en.json"):
            continue
        src = directory + filename
        if parent_id_not_exist(src):
            selected_json.append(src[:-5] + "_usersays_en.json")
    return selected_json

def cleaning_text(text):
    text = re.sub(r"\W+", " ", text.lower())
    end = "(?![a-z0-9])"
    first = "(?<![a-z0-9])"
    patterns = [{"regex": "sy[a-z]*", "repl": "saya "},
                {"regex": "min", "repl": "admin "},
                {"regex": "delivered", "repl": "terkirim "},
                {"regex": "krn[a-z]*", "repl": "karena "},
                {"regex": "edit", "repl": "ubah "},
                {"regex": "input", "repl": "masukan "},
                {"regex": "update", "repl": "perbarui "},
                {"regex": "dg", "repl": "dengan "},
                {"regex": "bgm", "repl": "bagaimana "},
                {"regex": "bs", "repl": "bisa "},
                {"regex": "tgl[a-z]*", "repl": "tapi "},
                {"regex": "n", "repl": "dan "},
                {"regex": "dcancel", "repl": "dibatalkan "},
                {"regex": "no", "repl": "nomor "},
                {"regex": "seler", "repl": "penjual "},
                {"regex": "tdk", "repl": "tidak "},
                {"regex": "spt", "repl": "seperti "},
                {"regex": "gpp", "repl": "tidak apa apa "},
                {"regex": "free", "repl": "gratis "},
                {"regex": "rata[0-9]*", "repl": "rata rata "},
                {"regex": "gt", "repl": "gitu "},
                {"regex": "pdhl[a-z]*", "repl": "padahal "},
                {"regex": "tlg[a-z]*", "repl": "tolong "}]
    for pattern in patterns:
        text = re.sub(first+pattern["regex"]+end, pattern["repl"], text.lower())
    return text

def generate_intent_json(selected_json, len_directory):
    rasa_json_format = {
        "rasa_nlu_data": {
            "common_examples": [],
            "regex_features": [],
            "lookup_tables": [],
            "entity_synonyms": []
        }
    }
    for json_file in selected_json:
        try:
            with open(json_file, 'r') as f:
                json_data = json.load(f)
                if len(json_data) < 10:
                    # print("'"+json_file[len_directory:-17]+"', ")
                    continue
                for obj in json_data:
                    text = ""
                    for data in obj["data"]:
                        text += data["text"]
                    rasa_json_format["rasa_nlu_data"]["common_examples"].append({"text": cleaning_text(text),
                                                                                "intent": json_file[
                                                                                        len_directory:-17].lower()})
        except OSError as e:
            continue
    return rasa_json_format

def generate_entity_json(directory, rasa_json_format):
    for filename in os.listdir(directory):
        if filename.endswith("_en.json"):
            src = directory + filename
            try:
                with open(src, 'r') as f:
                    json_data = json.load(f)
                    for obj in json_data:
                        rasa_json_format["rasa_nlu_data"]["entity_synonyms"].append(obj)
            except OSError as e:
                continue
    return rasa_json_format

def convert_df_to_rasa_standard(directory):
    intents = directory + "/intents/"
    selected_file = select_json_file(intents)
    rasa_json = generate_intent_json(selected_file, len_directory=len(intents))
    entities = directory + "/entities/"
    rasa_json = generate_entity_json(entities, rasa_json)
    return rasa_json

def create_json_file(file, data):
    with open(file, 'w') as outfile:
        json.dump(data, outfile,  sort_keys=True, indent=4)

def argv_command_line(argv):
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv, "d:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print('test.py -d <folderdialogflow> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('test.py -d <folderdialogflow> -o <outputfile>')
            sys.exit()
        elif opt in ("-d", "--data"):
            inputfile = arg
        elif opt in ("-o", "--output"):
            outputfile = arg
    if inputfile == '' or outputfile == '':
        print('test.py -d <folderdialogflow> -o <outputfile>')
        sys.exit(2)
    print('Input file is "', inputfile)
    print('Output file is "', outputfile)
    return inputfile, outputfile

def main(argv):
    inputfile, outputfile = argv_command_line(argv)
    # Diretory export file dialogflow
    directory = inputfile
    # -----------------------------------------------------#
    # Begin convert dialog flow to rasa standard json'
    json = convert_df_to_rasa_standard(directory)
    create_json_file(outputfile, json)


if __name__ == "__main__":
    main(sys.argv[1:])


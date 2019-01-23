import os
import sys, getopt

def rename_file_to_en(directory):
    for filename in os.listdir(directory):
        if filename.endswith("_id.json"):
            new_file_name = filename[:-8] + "_en.json"
            src = directory + filename
            dst = directory + new_file_name
            os.rename(src, dst)


def delete_file(directory, persist_file):
    for filename in os.listdir(directory):
        if filename.startswith(tuple(persist_file)):
            dst = directory + filename
            os.remove(dst)
            continue


def convert_df_id_to_en(directory):
    rename_file_to_en(directory + "/entities/")
    rename_file_to_en(directory + "/intents/")

def argv_command_line(argv):
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv, "d:r:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print('test.py -d <folderdialogflow> -r <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('test.py -d <folderdialogflow> -r <outputfile>')
            sys.exit()
        elif opt in ("-d", "--data"):
            inputfile = arg
        elif opt in ("-r", "--remove"):
            outputfile = arg
    if inputfile == '' or outputfile == '':
        print('test.py -d <folderdialogflow> -r <outputfile>')
        sys.exit(2)
    print('Input file is "', inputfile)
    print('Output file is "', outputfile)
    return inputfile, outputfile

def main(argv):
    rename, delete = argv_command_line(argv)
    # Diretory export file dialogflow
    directory = rename
    convert_df_id_to_en(directory)
    #-----------------------------------------------------#
    #DELETE all file except start with list of 'persist_file'
    # persist_file = ["smalltalk", "FAQ", "Account", "Logistic"]
    # delete_file(directory+"/intents/", persist_file)

if __name__ == "__main__":
    main(sys.argv[1:])

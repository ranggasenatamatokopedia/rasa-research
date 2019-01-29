import nltk
import jellyfish
import re
import csv
from tqdm import tqdm
from nltk.util import ngrams
from spreadsheet_writer import SpreadsheetWriter

# This function will return if string is similar or not based on several edit distance
def checkIsSimilar(ori, typo):
    # TODO adjust accordingly
    th_ed = 2
    th_jd = 0.25
    th_jar = 0.9

    ed = nltk.edit_distance(ori, typo)
    jd = nltk.jaccard_distance(set(ori), set(typo))
    # lev = jellyfish.levenshtein_distance(ori, typo)
    jar = jellyfish.jaro_distance(ori, typo)
    # dam = jellyfish.damerau_levenshtein_distance(ori, typo)
    if (jd < th_jd and jd > 0) and (ed < th_ed and ed > 0) and (jar > th_jar and jar < 1):
        # print(ori, typo, jd, ed, lev, jar, dam)
        # remove punctuations and check if it's the same
        n_ori = re.sub(r'[^\w\s]','',ori)
        n_typo = re.sub(r'[^\w\s]','',typo)
        if n_ori != n_typo:
            n_key = n_ori + ',' + n_typo
            return True, n_key, jd, ed, jar
    
    return False, ori + ',' + typo, jd, ed, jar

OUTPUT_WORKSHEET_FILENAME = 'String Similarity Data.xlsx'
SHEET_ENTITY = 'Entities'
SHEET_DATA = 'Data'
SHEET_OTHER = 'Other Data'
SHEET_DF_ENTITIES = 'DF Entities'
ss_writer = SpreadsheetWriter()

ss_writer.create_workbook(OUTPUT_WORKSHEET_FILENAME,[
    SHEET_ENTITY,
    SHEET_DATA,
    SHEET_OTHER,
    SHEET_DF_ENTITIES,
])

var_ngram = ['Abu-abu Muda','Merah',
'Titanium','Hijau Tosca','Ivory','Kuning',
'Perak','Cokelat','Fuchsia','Hitam',
'Ungu','Putih','Merah Salem','Merah Muda',
'Biru Muda','Hijau muda','Navy','Emas',
'Cokelat Muda','Abu-abu','Maroon','Turquoise',
'Beige','Tembaga','Biru','Hijau','Orange',
'Ready', 'Siap', 'ada']

var_bigram = ['32','40','42','34','36','38','29','30','S','31',
'32','36','38','XS','34','XL','M','L','XXXL','28','27','35','39','XXL','37','33',
'40','XXXL','27','L','29','XXL','37','25','S','35','M','26','28','30','36','33',
'XL','32','24','31','34','XS','8','6','9','5','14','7','10','13','12','15',
'11','16','L','8','2','M','10','0','8','4','6','14','XXS','4','12','XL',
'S','12','XXL','6','10','XS','35','44','43','37','46','40','45','47','39','41',
'42','38','36','39','26','30','32','37','29','36','31','33','38','25','34','35',
'27','28','24']

var_ngram = list(set(var_ngram))
var_bigram = list(set(var_bigram))

# must include spaces
prefix = [ 'size ','sz ','ukuran ','ukurn ','ukrn ','uk ']

with open('csv/text_variant.csv', 'r', encoding = "ISO-8859-1") as f:
    rows = list(csv.reader(f, delimiter=','))
    
    data = ""
    print("======= Loading csv files")
    text_list = {}
    for i, row in tqdm(enumerate(rows),total=len(rows)):
        if i == 0 or len(row) <3:
            continue

        # TODO remove limit later
        if i > 100000:
            break

        line = row[2].lower()
        if len(line) > 128 or len(line) == 0:
            continue
        data = data + ' ' + row[2]
        n_line = re.sub(r'[^\w\s]','',line)
        if not n_line in text_list.keys():
            text_list[n_line] = line
        i = i + 1
    
    data = data.lower()
    tokenize = nltk.word_tokenize(data)
    bigrams = ngrams(tokenize,2)

    print("======= Total Token", len(tokenize))

    typo_token_result = {}
    token_list = []

    isSimilar = False
    # check for warna
    print("======= Processing variant warna")
    for warna in tqdm(var_ngram,total=len(var_ngram)):
        warna = warna.lower()
        typo_token_result[warna+','+warna] = [warna, warna, 'warna']
        token_list.append(warna)
        for word in tokenize:
            isSimilar, n_key, jd, ed, jar = checkIsSimilar(warna, word)
            if isSimilar:
                if not n_key in typo_token_result.keys():
                    typo_token_result[n_key] = [warna, word, 'warna']
                    token_list.append(word)
                    # print(warna, word, jd, ed, jar)

    # check for size with prefix
    print("======= Processing variant size")
    for pref in tqdm(prefix,total=len(prefix)):
        for size in tqdm(var_bigram,total=len(var_bigram)):
            size = pref + size.lower()
            typo_token_result[size+','+warna] = [size, size, 'size']
            token_list.append(size)
            for gram in bigrams:
                word = gram[0] + ' ' + gram[1]
                word = word.lower()
                isSimilar, n_key, jd, ed, jar = checkIsSimilar(size, word)
                if isSimilar:
                    if not n_key in typo_token_result.keys():
                        typo_token_result[n_key] = [size, word, 'size']
                        token_list.append(word)
                        # print(size, word, jd, ed, jar)

    token_list = list(set(token_list))
    
    print("======= Processing text list")
    token_text = []
    other_text = []
    list_text = list(text_list.values())
    for text in tqdm(list_text,total=len(list_text)):
        if any(token in text for token in token_list):
            token_text.append([text])
        else:
            other_text.append([text])

    ss_writer.write_to_sheet(SHEET_ENTITY, ["Word", "Typo", "Group"], list(typo_token_result.values()))
    ss_writer.write_to_sheet(SHEET_DATA, ["Text"], token_text)
    ss_writer.write_to_sheet(SHEET_OTHER, ["Text"], other_text)

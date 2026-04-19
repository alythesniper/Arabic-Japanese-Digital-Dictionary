import csv
import json
import datetime 
import os
import zipfile
import re

def create_yomitan_zip(dictionary_name):
    '''
    Create the yomitan dictionary zip file in the working directory named the dictionary name.
    Expects the file structure created by create_term_bank_files() and must be ran in the parent directory
    of the directory created by create_term_bank_files().
    
    Args:
        dictionary_name (str): Name of the dictionary.

    Returns:
        bool: failed or succeeded
    '''
    files = os.listdir(f'./{dictionary_name}')
    with zipfile.ZipFile(f'{dictionary_name}.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in files:
            zipf.write(f'./{dictionary_name}/' + file, arcname=file)

def create_tag_bank(dictionary_name):
    '''
    Create tag bank file in a subfolder of the working directory named the dictionary name.
    
    Args:
        dictionary_name (str): Name of the dictionary.

    Returns:
        bool: failed or succeeded
    '''
    tag_bank = [
        [
            "v",
            "partOfSpeech",
            -1,
            "verb",
            1
        ],
        [
            "n",
            "partOfSpeech",
            -1,
            "noun",
            1
        ]
    ]
    with open(f"{dictionary_name}\\tag_bank_1.json", "w+", encoding='utf-8') as file:
        json.dump(tag_bank, file, ensure_ascii=False, indent=4)
    
    return True

def crate_index_file(dictionary_name):
    '''
    Create index.json file in a subfolder of the working directory named the dictionary name.
    
    Args:
        dictionary_name (str): Name of the dictionary.

    Returns:
        bool: failed or succeeded
    '''
    date = str(datetime.datetime.now().date()).replace("-", ".", 3)

    index_file = {
    "title": dictionary_name,
    "revision": date,
    "sequenced": True,
    "format": 3,
    "author": "Al-Ard",
    "indexUrl": "",
    "downloadUrl": "",
    "url": "https://www.arabic-japanese.com/",
    "description": "内藤浩二のアラビア語－日本語電子辞書をヨミタンへ。",
    "attribution": "内藤浩二",
    "sourceLanguage": "ara",
    "targetLanguage": "ja",
    "frequenceyMode": ""
    }
    with open(f"{dictionary_name}\\index.json", "w+", encoding='utf-8') as file:
        json.dump(index_file, file, ensure_ascii=False, indent=4)
    
    return True

def create_term_bank_files(dictionary_name, dictionary_array):
    '''
    Create term bank files in the working directory under the dictionary name.
    
    Args:
        dictionary_name (str): Name of the dictionary.
        dictionary_array (array[array[str]]): The array containing the dictionary entries.

    Returns:
        bool: failed or succeeded
    '''
    chunk_size = 8000
    file_count = 0
    # Make path if doesn't exist
    dir_path = f"{dictionary_name}\\"
    os.makedirs(dir_path, exist_ok=True) 

    for i in range(0, len(dictionary_array), chunk_size):
        file_count += 1
        chunk = dictionary_array[i:i + chunk_size]
        with open(f"{dictionary_name}\\term_bank_{file_count}.json", "w+", encoding='utf-8') as file:
            json.dump(chunk, file, ensure_ascii=False, indent=4)
    
    return True

# POS classes
noun_classes = ["【名】","【形】","【数】","【代】","【人代】","【関代】","【関副】","【不定代名詞】","【人名】","【名扱い】","【複】","【双】","【序】","【定冠詞】","【名［ⅣM］】","【ⅡM】","【Ⅷ M】","【Ⅷ】","【Ⅵ】","【Ⅴ】","【Ⅹ】","【Ⅹ受分】","【形】","細身の"]
verb_classes = ["【動】","【命】"]
other_classes = ["【例文】","【アルファベット】","【表現】","【間】","【副】","【疑】","【前】","【例文】","【表現】","【肯定詞】","【熟】","【諺】","【文例】","【接】","【例文】","【副・接】","【構文】","【接頭辞】","【表現","【例文,","【表現】","【例文】","１．（","【例文】","【Ⅴ】","【ⅡM】","１．片","【用例】","【表現 】","【集】","【表現不快な思いで、不愉快な記憶】","【接頭詞】","【ا表現】","【人代（接尾形）】","【否定詞】","【感嘆詞】","【願望詞】","【不定代名詞】","～より","【表現】","【表現",]

yomitan_dict = []

with open("./Dictionary Data/ar-ja-middle.csv", "r", encoding='utf-16') as file:
    raw_file = csv.reader(file, delimiter=',', quotechar='"')

    total_term_count = 0
    good_term_count = 0
    example_sentence_count = 0
    phrase_count = 0
    verb_count = 0
    noun_count = 0

    # Remove first entry as it is key for data
    next(raw_file)

    for raw_entry in raw_file:
        
        # If main term and defenition not present or defenition empty
        if len(raw_entry) < 2 or raw_entry[1] == "":
            total_term_count += 1
            continue
        else:
            total_term_count += 1
            good_term_count += 1

        # If reading not present
        if len(raw_entry) < 7:
            reading = ""
            headword = raw_entry[0]
            defenition = raw_entry[1]

            # Remove all non arabic letter + kashida (ـ), leaves '-' & ',' characters
            headword = re.sub(r"[^\u0621-\u063A\u0641-\u064A\u064B-\u0652\u0020\u002D\u002C]", "", headword)
        # If reading present
        else:
            headword = raw_entry[0]
            defenition = raw_entry[1]
            reading = raw_entry[6]

            # Remove all non arabic letter + kashida (ـ), leaves '-' & ',' characters
            if '例文' in defenition:
                headword = re.sub(r"[^\u0621-\u063A\u0641-\u064A\u064B-\u0652\u0020\u002D\u002C]", "", headword)
                reading = re.sub(r"[^\u0621-\u063A\u0641-\u064A\u064B-\u0652\u0020\u002D\u002C]", "", reading)
                example_sentence_count += 1
            elif '表現' in defenition:
                headword = re.sub(r"[^\u0621-\u063A\u0641-\u064A\u064B-\u0652\u0020\u002D\u002C]", "", headword)
                reading = re.sub(r"[^\u0621-\u063A\u0641-\u064A\u064B-\u0652\u0020\u002D\u002C]", "", reading)
                phrase_count += 1
            else:
                # Remove all non arabic letter + kashida (ـ), leaves '-' & ',' characters
                headword = re.sub(r"[^\u0621-\u063A\u0641-\u064A\u064B-\u0652\u002D\u002C]", "", headword)
                reading = re.sub(r"[^\u0621-\u063A\u0641-\u064A\u064B-\u0652\u002D\u002C]", "", reading)     

            # Scan reading for '-', then substring up to it
            seperator_index = -1
            try:
                seperator_index = reading.index('-')
                # Remove whitespace before seperator
                if reading[seperator_index-1] == ' ':
                    seperator_index -= 1
                reading = reading[0:seperator_index]
            except ValueError:
                try:
                    seperator_index = reading.index(',')
                    # Remove whitespace before seperator
                    if reading[seperator_index-1] == ' ':
                        seperator_index -= 1
                    reading = reading[0:seperator_index]
                except ValueError:
                    seperator_index = -1
                    reading = reading[0:]

            # Scan headword for '-', then substring up to it
            seperator_index = -1
            try:
                seperator_index = headword.index('-')
                # Remove whitespace before seperator
                if headword[seperator_index-1] == ' ':
                    seperator_index -= 1
                headword = headword[0:seperator_index]
            except ValueError:
                try:
                    seperator_index = headword.index(',')
                    # Remove whitespace before seperator
                    if headword[seperator_index-1] == ' ':
                        seperator_index -= 1
                    headword = headword[0:seperator_index]
                except ValueError:
                    seperator_index = -1
                    headword = headword[0:]


        
        # Reconstruct POS marker before getting POS
        try:
            end_index = defenition.index('】')+1
        except:
            reconstructed_pos = defenition[0:3]+'】'
            if reconstructed_pos in noun_classes or reconstructed_pos in verb_classes or reconstructed_pos in other_classes:
                defenition = defenition[0:3]+'】 ' + defenition[3:]
            end_index = 3

        # Get POS/grammatical class
        if defenition[0:end_index] in verb_classes:
            word_class = 'v'
            verb_count += 1
        else:
            word_class = 'n'
            noun_count += 1

        # Get word tags
        word_tags = word_class
       
        # Construct entry
        yomitan_entry = [
            headword,                   # Expression (term) 0
            reading,                    # Reading 1
            word_tags,                  # word class for gui 2
            word_class,                 # word class for arabic-transforms.js 3
            0,                          # Score 4
            [defenition],               # Definition 5
            good_term_count,            # Sequence 6
            ""                          # Tags 7
        ]
        yomitan_dict.append(yomitan_entry)
        

dictionary_name = 'アラビア語－日本語電子辞書'

create_term_bank_files(dictionary_name, yomitan_dict)

crate_index_file(dictionary_name)

create_tag_bank(dictionary_name)

create_yomitan_zip(dictionary_name)

print("Completed.")
print(f"Total of {good_term_count} good terms.")
print(f"Total of {verb_count} verbs.")
print(f"Total of {noun_count-phrase_count} nouns.")
print(f"Total of {phrase_count} phrases.")
print(f"Total of {example_sentence_count} example sentences.")
print(f"Total of {total_term_count - good_term_count} terms droped.")
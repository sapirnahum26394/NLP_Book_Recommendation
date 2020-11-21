import xml.etree.ElementTree as ET
import re


from gensim.models import Word2Vec


def parse_xml(xml_name):
    # xml should be in shape of a collection with some records
    xml_tree = ET.parse(xml_name)
    xml_root = xml_tree.getroot()
    fields_and_ids = []
    for record in xml_root:
        mms_id = ''
        fields = []
        fields_and_id = []
        for field in record.findall('controlfield'):
            if(field.get('tag') == '001'):
                mms_id = field.text
                break

        for field in record.findall('datafield'):
            if(field.get('tag') == '650'):
                for subfield in field.findall('subfield'):
                    fields.append(subfield.text)

        if(fields):
            fields_and_id.append(mms_id)
            fields_and_id.append(fields)
            fields_and_ids.append(fields_and_id)
    print fields_and_ids
    return fields_and_ids

def normalize_650_fields(records_list,dictionary):
    for record in records_list:
        for i, subfield in enumerate(record[1]):
            record[1][i] = re.sub(r'\[[0-9]*\]', '', subfield)
            record[1][i] = record[1][i].lower()
            record[1][i] = re.sub(r'\d', ' ', record[1][i])
            record[1][i] = re.sub(r'\s+', ' ', record[1][i])
            record[1][i] = re.sub(r'\.', '', record[1][i])
            record[1][i] = re.sub(r'\-', ' ', record[1][i])
            if "(" not in record[1][i]:
                dictionary[record[1][i]] = 0

    return "";
def separate_to_tokens(dictionary):
    dict=[]
    for key in dictionary:
        words = key.split()
        for word in words:
            if word not in dict:
                dict.append(word)
    return dict

def generate_records_vectors(normalized_list):
    for token in normalized_list:
        normalized_list[token]= Word2Vec(token, min_count=1)
    return normalized_list

def get_recommended_records(records_vectors,book_topic):
    return "";

def main():
    dictionary = {}
    records_list = parse_xml("bib records.XML")
    normalized_list = normalize_650_fields(records_list,dictionary)
    dictionary = separate_to_tokens(dictionary)
    # dictionary=generate_records_vectors(dictionary)
    print dictionary
    model = Word2Vec(dictionary, min_count=1)
    words=model.wv.vocab
    print words
    print model.wv['mistresses']
    print model.wv.most_similar('detective')
    # records_vectors = generate_records_vectors(normalized_list)
    # print('Enter required book topic:')
    # book_topic = input()
    # recommended_books = get_recommended_records(records_vectors,book_topic)
    # print(recommended_books)

if __name__ == "__main__":
    main()
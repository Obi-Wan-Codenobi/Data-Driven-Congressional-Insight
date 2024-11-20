import os
import re
from typing import Dict, List
import xml.etree.ElementTree as ET
from utils.load_bills_data import Bill_file
from .tftypes import TFTYPES
# Process all files in a given directory, extracting the following information for each file:
# Return: documents{TITLE, TITLE_LENGTH, BODY_COUNT, BODY_LENGTH}
#         total_number_of_docs
#         term_freq - the number of documents that contain a term

class Document:
    def __init__(self, id, title, title_length, body_hits, body_length, body, file_path):
        self.id = id
        self.title = title
        self.title_length = title_length
        self.body_hits = body_hits
        self.body_length = body_length
        self.body = body
        self.file_path = file_path
    
    def to_dict(self):
        return {
            "title": self.title
        }


def xml_to_text(xml_file, output_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    with open(output_file, "w") as file:
        def extract_text(element, indent=0):
            if element.text:
                file.write(element.text.strip() + "\n")

            for child in element:
                extract_text(child, indent + 2)
        extract_text(root)
        
def load_xml_to_text(bills : Dict[str,Bill_file], store_text_path):
    directory = os.path.dirname(store_text_path)
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
    
    skipped = 0
    writtten = 0
    for bill_name, bill in bills.items():
        file_name = os.path.basename(bill.file_path)
        text_file = os.path.splitext(file_name)[0] + '.txt'
        text_file_path = store_text_path + text_file
        if not os.path.exists(text_file_path):
            xml_to_text(bill.file_path, text_file_path)
            writtten+=1
        else:
            skipped+=1
            
        bill.file_path = text_file_path
    print(f"{writtten} text files written.\n{skipped} text files found")

        


def get_document_data(file_path):
    files = []
    for root, dirs, filenames in os.walk(file_path):
        for filename in filenames:
            full_path = os.path.join(root, filename)
            files.append(full_path)

    documents: List[Document] = []
    total_number_of_docs = 0
    docs_with_term = {}
    
    id:int =0
    for file in files:
        id+=1
        total_number_of_docs += 1
        written_title = False
        document = {}
        body_hits = {}
        current_index = 0

        try:
            with open(file, 'r') as f:
                body=""
                for line in f:
                    body+=line
                    line = line.strip()
                    
                    # Includes words and numbers
                    if not written_title and bool(re.search(r'\w+', line.lower())):
                        document["TITLE"] = line
                        document["TITLE_LENGTH"] = len(line)
                        written_title = True
                        continue
                        
                    # Includes words and numbers
                    words = re.findall(r'\w+', line.lower())
                    for word in words:
                        if word not in body_hits:
                            body_hits[word] = []  
                        body_hits[word].append(current_index)  # Store the current index
                        current_index += len(word) + 1  # Update index (add 1 for space or punctuation)
                document["BODY"] = body
                document["BODY_HITS"] = body_hits
                document["BODY_LENGTH"] = current_index  
                documents.append(Document(id, document["TITLE"], document["TITLE_LENGTH"], document["BODY_HITS"], document["BODY_LENGTH"], document["BODY"], file))
                
                
                # for word in document["TITLE"].lower().split():
                #     term_freq[TFTYPES[0]][word] = term_freq[TFTYPES[0]].get(word, 0) + 1
                    
                # for key in body_hits.keys():
                #     term_freq[TFTYPES[1]][key] = term_freq[TFTYPES[1]].get(key, 0) + 1
                
                for key in body_hits.keys():
                    docs_with_term[key] = docs_with_term.get(key,0) + 1
                    
        except IOError as e:
            print(f"Error reading file {file}: {e}")
    
    print(f"{id} Documents loaded...")
    return documents, docs_with_term, total_number_of_docs
                    
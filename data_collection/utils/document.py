import os
import re
from typing import List
from .tftypes import TFTYPES
# Process all files in a given directory, extracting the following information for each file:
# Return: documents{TITLE, TITLE_LENGTH, BODY_COUNT, BODY_LENGTH}
#         total_number_of_docs
#         term_freq - the number of documents that contain a term

class Document:
    def __init__(self, title, title_length, body_hits, body_length, body):
        self.title = title
        self.title_length = title_length
        self.body_hits = body_hits
        self.body_length = body_length
        self.body = body
    
    def to_dict(self):
        return {
            "title": self.title
        }

def get_document_data(file_path):
    files = []
    for root, dirs, filenames in os.walk(file_path):
        print(f"Found file: {filenames}")
        for filename in filenames:
            full_path = os.path.join(root, filename)
            files.append(full_path)

    documents: List[Document] = []
    total_number_of_docs = 0
    docs_with_term = {}
    
    for file in files:
        total_number_of_docs += 1
        written_title = False
        document = {}
        body_hits = {}
        current_index = 0

        try:
            with open(file, 'r') as f:
                for line in f:
                    line = line.strip()
                    
                    # Includes words and numbers
                    if not written_title and bool(re.search(r'\w+', line.lower())):
                        document["TITLE"] = line
                        document["TITLE_LENGTH"] = len(line)
                        written_title = True
                    
                    # Includes words and numbers
                    words = re.findall(r'\w+', line.lower())
                    for word in words:
                        if word not in body_hits:
                            body_hits[word] = []  
                        body_hits[word].append(current_index)  # Store the current index
                        current_index += len(word) + 1  # Update index (add 1 for space or punctuation)
                document["BODY"] = words
                document["BODY_HITS"] = body_hits
                document["BODY_LENGTH"] = current_index  
                documents.append(Document(document["TITLE"], document["TITLE_LENGTH"], document["BODY_HITS"], document["BODY_LENGTH"], document["BODY"]))
                
                
                # for word in document["TITLE"].lower().split():
                #     term_freq[TFTYPES[0]][word] = term_freq[TFTYPES[0]].get(word, 0) + 1
                    
                # for key in body_hits.keys():
                #     term_freq[TFTYPES[1]][key] = term_freq[TFTYPES[1]].get(key, 0) + 1
                
                for key in body_hits.keys():
                    docs_with_term[key] = docs_with_term.get(key,0) + 1
                    
        except IOError as e:
            print(f"Error reading file {file}: {e}")
            
    return documents, docs_with_term, total_number_of_docs
                    
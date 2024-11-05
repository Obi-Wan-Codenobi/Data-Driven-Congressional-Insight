import os
import re

# Process all files in a given directory, extracting the following information for each file:
# Return: documents{TITLE, TITLE_LENGTH, BODY_COUNT, BODY_LENGTH}
#         total_number_of_docs
#         term_freq - the number of documents that contain a term


def get_document_data(file_path):
    files = []
    for root, dirs, filenames in os.walk(file_path):
        for filename in filenames:
            full_path = os.path.join(root, filename)
            files.append(full_path)
    
    documents = []
    total_number_of_docs = 0
    term_freq = {}
    for file in files:
        total_number_of_docs +=1
        
        written_title = False
        document = {}
        with open(file, 'r') as f:
            body = {}
            for line in f:
                line = line.strip()
                if not written_title and bool(re.search(r'\w+', line)):
                    document ["TITLE"] = line
                    document ["TITLE_LENGTH"] = len(line)
                    written_title = True
                
                # Includes words and numbers
                words = re.findall(r'\w+', line.lower())
                for word in words:
                    if word not in body:
                        body[word] = 1
                    else:
                        body[word] += 1
                        
                    
        
            document["BODY_COUNT"] = body 
            document["BODY_LENGTH"] = len(body)
            documents.append(document)
            
            for key, value in body.items():
                term_freq[key] = term_freq.get(key, 0) + 1
            
        
    return documents, term_freq , total_number_of_docs
                    
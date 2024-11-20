import os
import sys
import time

sys.path.append(os.path.abspath('../'))
sys.path.append(os.path.abspath('../data_collection'))



#small_bill_data_directory = "./../data_collection/bill_texts/"
data_directory = "./../data/congres-repo/data"
saved_data_tmp_path = "./../data_collection/tmp/"

from data_collection.utils.document import get_document_data, Document
from data_collection.main import get_bill_documents
from data_collection.main import get_vote_documents

start = time.time()
bills = get_bill_documents(data_directory, saved_data_tmp_path)
votes = get_vote_documents(data_directory)
document_data = get_document_data(saved_data_tmp_path)



def query_bm25(query: str):
    from data_collection.main import executeBM25
    return executeBM25(query, document_data)

def top_ten_documents(document_scores):
    top_scores = sorted(document_scores, key=lambda x: x[1], reverse=True)[:10]
    return top_scores

def to_json(document_scores):
    json  = [{"document": doc.to_dict(), "id": doc.id} for doc, score in document_scores]
    return json

def document_id_to_vote():
    document_vote_data = {}
    bills_keys = set(bills.keys()) if bills else set()
    votes_keys = set(votes.keys()) if votes else set()

    common_keys = bills_keys & votes_keys
    
    for key in common_keys:
        bill = bills.get(key)
        bill = bills.get(key)
        if bill is None:
            continue
        for doc in document_data[0]:
            if doc.file_path==bill.file_path:
                document_vote_data[doc.id] = key
    
    return document_vote_data

end = time.time()
print(f"All data loaded: {float((end-start)/60)} minutes")
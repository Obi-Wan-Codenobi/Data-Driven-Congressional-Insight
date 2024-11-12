import os
import sys

sys.path.append(os.path.abspath('../'))
sys.path.append(os.path.abspath('../data_collection'))



small_bill_data_directory = "./../data_collection/bill_texts/"
from data_collection.utils.document import get_document_data, Document
document_data = get_document_data(small_bill_data_directory)

def query_bm25(query: str):
    from data_collection.main import executeBM25
    return executeBM25(query, document_data)

def top_ten_documents(document_scores):
    top_scores = sorted(document_scores, key=lambda x: x[1], reverse=True)[:10]
    return top_scores

def to_json(document_scores):
    json  = [{"document": doc.to_dict(), "score": score} for doc, score in document_scores]
    return json
        
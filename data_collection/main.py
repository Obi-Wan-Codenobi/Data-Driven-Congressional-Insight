import sys
import re
import argparse
from utils.initiate_bill_load import initiate_bill_load
from utils.load_vote_data import load_and_merge_all_votes
from utils.bm25 import BM25
from utils.dumbyloader import *
from utils.document import get_document_data, load_xml_to_text
from utils.load_bills_data import load_and_merge_all_bills
from utils.tftypes import TFTYPES
import os
import time

# this is for the api to import and use
def executeBM25(input:str, document_data):
    query = Query(input)
    documents, docs_with_term, total_number_of_docs = document_data
    scorer = BM25(documents, docs_with_term, total_number_of_docs, query)
    scored_documents = scorer.score_documents()
    scored_documents.sort(key=lambda x: x[1], reverse=True)
    return scored_documents

def get_bill_documents(root_path):
    directories = []
    for item in os.listdir(root_path):
        item_path = os.path.join(root_path, item)
        if os.path.isdir(item_path):
            bills_path = os.path.join(item_path, "bills")
            if os.path.isdir(bills_path):
                directories.append(bills_path)

    print(directories)
    bills = load_and_merge_all_bills(directories)
        
    return bills

def get_vote_documents(root_path):
    directories = []
    for item in os.listdir(root_path):
        item_path = os.path.join(root_path, item)
        if os.path.isdir(item_path):
            bills_path = os.path.join(item_path, "votes")
            if os.path.isdir(bills_path):
                directories.append(bills_path)

    print(directories)
    votes = load_and_merge_all_votes(directories)
    return votes

# For testing
def main():
    
    arg = input("Convert xml data to txt? Type: '1' (yes) or '0'(no)")
    if arg:
        #convert data
        path = "./../data/congres-repo/data"
        bills = get_bill_documents(path)
        
        votes = get_vote_documents(path)

        bills_keys = set(bills.keys()) if bills else set()
        #votes_keys = set(votes.keys()) if votes else set()

        #common_keys = bills_keys & votes_keys
        #print(f"Intersected keys: {len(common_keys)}")
        print('WRITING')
        load_xml_to_text(bills, "./tmp/")
        
        # test query
        document_data = get_document_data("./tmp/")
        user_query = input("What topic would you like to reference? ")
        scored_documents = executeBM25(user_query, document_data)
        top_x = 5  
        for i in range(min(top_x, len(scored_documents))):
            doc, score = scored_documents[i]
            print(f"Document: {doc.title}, Score: {score}")
        
        
        
        
        sys.exit()
    
    
    small_bill_data_directory = "./bill_texts"
    document_data = get_document_data(small_bill_data_directory)
   
    user_query = input("What topic would you like to reference? ")
    scored_documents = executeBM25(user_query, document_data)
    
    top_x = 5  
    for i in range(min(top_x, len(scored_documents))):
        doc, score = scored_documents[i]
        print(f"Document: {doc.title}, Score: {score}")

   

    sys.exit()

if __name__ == "__main__":
    main()

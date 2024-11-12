import sys
import re
import argparse
from utils.initiate_bill_load import initiate_bill_load
from utils.load_vote_data import load_vote_data
from utils.bm25 import BM25
from utils.dumbyloader import *
from utils.document import get_document_data
from utils.load_bills_data import load_bill_data
from utils.tftypes import TFTYPES

# this is mainly for the api to import and use

def executeBM25(input:str, document_data):
    query = Query(input)
    documents, docs_with_term, total_number_of_docs = document_data
    scorer = BM25(documents, docs_with_term, total_number_of_docs, query)
    scored_documents = scorer.score_documents()
    scored_documents.sort(key=lambda x: x[1], reverse=True)
    return scored_documents

def main(args):
    arg = input("Convert xml data to txt? Type: '1' (yes) or '0'(no)")
    if args.c:
        #convert data
        bills_path = "./../data/congres-repo/data/118/bills"
        files = load_bill_data(bills_path)
        sys.exit()
    
    # file_prefix = "./../../congress/data/118/votes/"
    
    # year_start = 2016
    # year_end = 2024
    
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
    parser = argparse.ArgumentParser(description="Check for optional argument -c.")
    parser.add_argument("-c", type=int, help="An optional integer value for the -c to convert data")

    args = parser.parse_args()
    
    main(args)

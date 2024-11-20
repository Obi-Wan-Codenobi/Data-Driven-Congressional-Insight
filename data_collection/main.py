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

def get_bill_documents(root_path, tmp_path):
    directories = []
    for item in os.listdir(root_path):
        item_path = os.path.join(root_path, item)
        if os.path.isdir(item_path):
            bills_path = os.path.join(item_path, "bills")
            if os.path.isdir(bills_path):
                directories.append(bills_path)

    bills = load_and_merge_all_bills(directories)
    load_xml_to_text(bills, tmp_path)
    return bills

def get_vote_documents(root_path):
    directories = []
    for item in os.listdir(root_path):
        item_path = os.path.join(root_path, item)
        if os.path.isdir(item_path):
            bills_path = os.path.join(item_path, "votes")
            if os.path.isdir(bills_path):
                directories.append(bills_path)

    votes = load_and_merge_all_votes(directories)
    return votes

# For testing
def test_ranking(scored_docs, benchmark):
    print("\nTesting Rank Results:")
    for bench in benchmark:
        test_title = bench["title"].strip()
        expected_rank = bench["rank"]
        # Find the document in the scored_documents
        bm25_result = next(
            (i + 1 for i, (doc, _) in enumerate(scored_docs) if doc.title == test_title), None
        )

        if bm25_result:
            print(f"Title: {test_title}, Expected Rank: {expected_rank}, BM25 Rank: {bm25_result}")
        else:
            print(f"Title: {bench['title']} not found in scored documents!")
        




def main():
    
    arg = input("Convert xml data to txt? Type: '1' (yes) or '0'(no)")
    if arg:
        #convert data
        path = "./../data/congres-repo/data"
        tmp_path = "./tmp/"
        bills = get_bill_documents(path, tmp_path)
        
        votes = get_vote_documents(path)

        # bills_keys = set(bills.keys()) if bills else set()
        # print(bills_keys)
        # print("\n\n\n")
        # votes_keys = set(votes.keys()) if votes else set()
        # print(votes_keys)
        # print("\n\n\n")

        # common_keys = bills_keys & votes_keys
        # print(common_keys)
        # print(f"Intersected keys: {len(common_keys)}")
        # sys.exit()
        
        print('WRITING')
        load_xml_to_text(bills, "./tmp/")
        
        # test query
        document_data = get_document_data("./tmp/")
        user_query = input("What topic would you like to reference? [To run test, Type covid]   ")
        scored_documents = executeBM25(user_query, document_data)
        top_x = 5  
        for i in range(min(top_x, len(scored_documents))):
            doc, score = scored_documents[i]
            print(f"Document: {doc.title}, Score: {score}")
        
        #Testing Ranking (usage on a covid query)
        benchmark = [
            {"title":"118 HR 117 IH: To prohibit any entity that receives Federal funds from the COVID relief packages from mandating employees receive a COVID–19 vaccine, and for other purposes.", "rank":1},
            {"title":"118 HR 1346 IH: COVID–19 Origin Act of 2023", "rank":2},
            {"title":"118 HR 1376 IH: COVID–19 Origin Act of 2023", "rank":3},
            {"title":"118 HR 301 IH: Unmasking the Origins of COVID–19 Act", "rank":4},
            {"title":"118 HR 991 IH: COVID–19 Vaccination Non-Discrimination Act", "rank":5},
            {"title":"118 HR 348 IH: Transparency in COVID–19 Expenditures Act", "rank":6},
            {"title":"118 HR 1621 IH: COVID–19 National Memorial Act", "rank":7},
            {"title":"118 HR 4761 IH: SAFE CAR Act", "rank":8},
            {"title":"107 HR 895 IH: Combating Organized Retail Crime Act of 2023", "rank":9},
            {"title":"118 HR 4899 IH: Housing Financial Literacy Act of 2023", "rank":10},
        ]
        if(user_query == "covid"):
            test_ranking(scored_documents, benchmark)
        
        
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

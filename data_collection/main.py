from utils.initiate_bill_load import initiate_bill_load
from utils.load_vote_data import load_vote_data
<<<<<<< HEAD
#from utils.load_bills_data import load_bill_data
from utils.document import get_document_data

def main():
    vote_data_file_prefix = "./../data/congres-repo/data/118/votes/"
    year_start = 2016
    year_end = 2024
    #load_vote_data(vote_data_file_prefix, year_start, year_end)
    
    bill_data_file_prefix ="./../data/congres-repo/data/118/bills/"
    #load_bill_data(bill_data_file_prefix)
    
    small_bill_data_directory ="./bill_texts"
    documents, term_freq , total_number_of_docs = get_document_data(small_bill_data_directory)
    
=======
from utils.bm25 import BM25
from utils.dumbyloader import *
import sys

def main():
    file_prefix = "./../../congress/data/118/votes/"
    test_folder = "../bill_texts/"
    year_start = 2016
    year_end = 2024
   
    user_query = input("What topic would you like to reference? ")
    query = StoreQuery(user_query)


    #load_vote_data(file_prefix, year_start, year_end) 
    #initiate_bill_load()


    


    #set up scorer
    #other = Utilities() #dummy fuction, will be incorperated if needed
    #scorer = BM25(other, test_folder)

    '''
    for document, score = bm25,get
    '''    
    sys.exit()


    


>>>>>>> main

if __name__ == "__main__":
    main()

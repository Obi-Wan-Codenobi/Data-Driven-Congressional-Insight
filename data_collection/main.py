from utils.initiate_bill_load import initiate_bill_load
from utils.load_vote_data import load_vote_data
from utils.bm25 import BM25
from utils.dumbyloader import *
import sys
from utils.document import get_document_data

def main():
    file_prefix = "./../../congress/data/118/votes/"
    test_folder = "../bill_texts/"
    year_start = 2016
    year_end = 2024
   
    user_query = input("What topic would you like to reference? ")
    query = StoreQuery(user_query)


    #load_vote_data(file_prefix, year_start, year_end) 
    #initiate_bill_load()


    
    small_bill_data_directory ="./bill_texts"
    documents, term_freq , total_number_of_docs = get_document_data(small_bill_data_directory)

    #set up scorer
    #other = Utilities() #dummy fuction, will be incorperated if needed
    #scorer = BM25(other, test_folder)

    '''
    for document, score = bm25,get
    '''    
    sys.exit()


    



if __name__ == "__main__":
    main()
    
from utils.initiate_bill_load import initiate_bill_load
from utils.load_vote_data import load_vote_data
from utils.bm25 import BM25
from utils.dumbyloader import *
import sys
from utils.document import get_document_data

def main():
    file_prefix = "./../../congress/data/118/votes/"
    
    year_start = 2016
    year_end = 2024
   
    user_query = input("What topic would you like to reference? ")
    query = StoreQuery(user_query)
    

    small_bill_data_directory = "./bill_texts"
    documents, _, total_number_of_docs = get_document_data(small_bill_data_directory)

    
    scorer = BM25(documents, {}, total_number_of_docs, query)

    
    #scorer.calculate_term_frequencies(documents)

    
    scored_documents = scorer.score_documents()
    scored_documents.sort(key=lambda x: x[1], reverse=True)

    
    top_x = 5  
    for i in range(min(top_x, len(scored_documents))):
        doc, score = scored_documents[i]
        print(f"Document: {doc['TITLE']}, Score: {score}")

   

    sys.exit()

if __name__ == "__main__":
    main()
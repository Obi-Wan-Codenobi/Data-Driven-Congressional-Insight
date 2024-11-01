from utils.initiate_bill_load import initiate_bill_load
from util.load_vote_data import load_vote_data



def main():
    file_prefix = "./../../congress/data/118/votes/"
    
    year_start = 2016
    year_end = 2024
   
    load_vote_data(file_prefix, year_start, year_end) 
    initiate_bill_load()

if __name__ == "__main__":
    main()

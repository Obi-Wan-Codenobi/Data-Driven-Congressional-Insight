from utils.initiate_bill_load import initiate_bill_load
from utils.load_vote_data import load_vote_data



def main():
    file_prefix = "./../../congress/data/118/votes/"
    test_folder = "../bill_texts/"
    year_start = 2016
    year_end = 2024
   
    user_query = input("What topic would you like to reference? ")

    load_vote_data(file_prefix, year_start, year_end) 
    initiate_bill_load()
    



if __name__ == "__main__":
    main()

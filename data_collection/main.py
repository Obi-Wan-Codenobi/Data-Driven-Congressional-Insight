from utils.initiate_bill_load import initiate_bill_load
from utils.load_vote_data import load_vote_data
from utils.load_bills_data import load_bill_data


def main():
    vote_data_file_prefix = "./../data/congres-repo/data/118/votes/"
    year_start = 2016
    year_end = 2024
    load_vote_data(vote_data_file_prefix, year_start, year_end)
    
    bill_data_file_prefix ="./../data/congres-repo/data/118/bills/"
    load_bill_data(bill_data_file_prefix)
    
    #initiate_bill_load()

if __name__ == "__main__":
    main()

import os
import json
import threading
import time
from collections import defaultdict


"""
all_votes = {bill_name : Votes -> casted_votes{voter_id : vote_type} }
"""
class Votes:
    def __init__(self, vote_name: str | None, file_path, date: str | None, casted_votes):
        self.vote_name = vote_name
        self.file_path = file_path
        self.date = date
        self.casted_votes: dict[str:str] = casted_votes
        
class Load_votes:

    def __init__(self):
        self.all_votes = {}
        self.errors = {}
        self.lock = threading.Lock()
        self.errors_lock = threading.Lock()


    def start_thread(self, dir):
        try:
            if os.path.exists(dir):
                directories = self.get_directories(dir)
            else:
                print(f"Directory does not exist: {dir}")

            for path in directories:
                json_path = os.path.join(path, 'data.json')
                if os.path.exists(json_path):
                    self.parseJsonVotes(json_path) 

        except Exception as e:
            print(f"Error in thread for {dir}: {e}")


    def parseJsonVotes(self, path):
        with open(path, 'r') as file:
            try:
                json_data = json.load(file)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON from {path}: {e}")
                return {}
        
        chamber = json_data.get("chamber")
        congress = json_data.get("congress")
        number = json_data.get("number")
        vote_name = f"{congress}{chamber}{number}"
        vote_count = {}
        
        bill_data = json_data.get("bill", {})
        bill_congress = bill_data.get("congress", "default_congress_value")
        bill_number = bill_data.get("number", "default_number_value")
        bill_type = bill_data.get("type", "default_bill_type")
        
        bill = f"{bill_congress}{bill_type}{bill_number}"
        date = json_data.get("date")
        
        for vote_type in ["Aye", "No", "Not Voting"]:
                voters = json_data.get("votes", {}).get(vote_type, [])
                
                for voter in voters:
                    display_name = voter.get("id")
                    if display_name and display_name not in vote_count:
                        vote_count[display_name] = vote_type
                    else:
                        error_msg = f"Error in path({path})\nFor display name: {display_name}, vote name: {vote_name}"
                        with self.errors_lock:
                            self.errors[vote_name] = error_msg
                        
        this_vote = Votes(vote_name, path, date, vote_count )
        with self.lock:
            self.all_votes[bill] = this_vote

    def get_directories(self, dir):
        directories = []
        for item in os.listdir(dir):
            if os.path.isdir(os.path.join(dir, item)):
                directories.append(os.path.join(dir, item))
        return directories
    
    def fetch(self, file_prefix:str):

        bills_data = self.get_directories(file_prefix)
        threads = []
        for i in bills_data:  
            thread = threading.Thread(target=self.start_thread, args=(i,))
            threads.append(thread)

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        
        with self.errors_lock:
            for vote, error in self.errors.items():
                print(f"Vote {vote} : error {error}")
        
        return self.all_votes


def load_and_merge_all_votes(directories):
    start = time.time()
    merged_data = {}
    lock = threading.Lock()
  
    def load_data_for_directory(directory):
        loader = Load_votes()
        data = loader.fetch(directory)
        with lock:
            merged_data.update(data)
            print(f"{len(data)} Bills found for {directory}")

    threads = []

    # new thread for each voting year
    for dir in directories:
        thread = threading.Thread(target=load_data_for_directory, args=(dir,))
        thread.start()
        threads.append(thread)


    for thread in threads:
        thread.join()
    end = time.time()

    print(f"{len(merged_data)} Votes found total")
    print(f"Time elasped: {float((end-start)/60)} minutes")
    print(f"Time elasped: {float((end-start))} seconds")
    return merged_data


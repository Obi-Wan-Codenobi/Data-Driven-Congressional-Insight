import os
from dotenv import load_dotenv
import json
from utils.fetch_data import fetch_data
import threading
import time
from collections import defaultdict
import matplotlib.pyplot as plt

load_dotenv()

politician_number_of_votes = {}
lock = threading.Lock()

document_count = 0
total_length = 0
document_lock = threading.Lock()

def start_thread(dir):
    try:
        if os.path.exists(dir):
            
            directories = []
            for item in os.listdir(dir):
                if os.path.isdir(os.path.join(dir, item)):
                    directories.append(os.path.join(dir, item))            
        else:
            print(f"Directory does not exist: {dir}")

        for path in directories:
            json_path = os.path.join(path, 'data.json')  
            if os.path.exists(json_path):
                vote_dict = parseJsonVotes(json_path) 
                merge_dictionaries(politician_number_of_votes, vote_dict)

                with document_lock:
                    global document_count, total_length
                    document_count += 1
                    with open(json_path, 'r') as file:
                        content = file.read()
                        total_length += len(content)  # Count characters

    except Exception as e:
        print(f"Error in thread for {dir}: {e}")

def merge_dictionaries(orginal_dict, new_dict):
    with lock:         
        for key, value in new_dict.items():
            orginal_dict[key] = orginal_dict.get(key, 0) + value


def parseJsonVotes(path):
    with open(path, 'r') as file:
        try:
            json_data = json.load(file)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from {path}: {e}")
            return {}

    vote_count = {}
    
    for vote_type in ["Aye", "No"]:
            voters = json_data.get("votes", {}).get(vote_type, [])
            
            for voter in voters:
                display_name = voter.get("display_name")
                if display_name:
                    vote_count[display_name] = vote_count.get(display_name, 0) + 1
    return dict(vote_count) 

def plot_vote_counts(vote_count):
    sorted_votes = dict(sorted(vote_count.items(), key=lambda item: item[1], reverse=True))
    top_politicians = list(sorted_votes.keys())[:20]
    top_counts = list(sorted_votes.values())[:20]
    plt.figure(figsize=(10, 6))
    bars = plt.barh(top_politicians, top_counts, color='skyblue')
    plt.xlabel('Number of Votes')
    plt.title('Top 20 Vote Counts per Politician')
    plt.xlim(0, max(top_counts) * 0.75)  
    plt.gca().invert_yaxis()  
    plt.show()



def load_vote_data(file_prefix:str, year_start:int, year_end:int ):
    voting_data = []
    
    for year in range(year_start, year_end + 1):
        voting_data.append(f'{file_prefix}{year}/')

    threads = []
    for i in voting_data:  
        thread = threading.Thread(target=start_thread, args=(i,))
        threads.append(thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    print("Final count of votes per politician:")
    for politician, count in politician_number_of_votes.items():
        print(f"{politician}: {count}")
    
    plot_vote_counts(politician_number_of_votes)

    print(len(politician_number_of_votes))

    
    print(f'Average length: {float(total_length/document_count)}')
    print(f'Number of documents: {document_count}')
    


   


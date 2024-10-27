import os
from dotenv import load_dotenv
import json
from util.fetch_data import fetch_data
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
                merge_and_count(vote_dict)

                with document_lock:
                    global document_count, total_length
                    document_count += 1
                    with open(json_path, 'r') as file:
                        content = file.read()
                        total_length += len(content)  # Count characters

    except Exception as e:
        print(f"Error in thread for {dir}: {e}")

def merge_and_count(new_dict):
    global politician_number_of_votes 
    with lock:         
        for key, value in new_dict.items():
            politician_number_of_votes[key] = politician_number_of_votes.get(key, 0) + value


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
    # Sort the dictionary by counts
    sorted_votes = dict(sorted(vote_count.items(), key=lambda item: item[1], reverse=True))
    
    # Prepare data for plotting: take only the top 100
    top_politicians = list(sorted_votes.keys())[:20]
    top_counts = list(sorted_votes.values())[:20]

    # Create a bar chart
    plt.figure(figsize=(10, 6))
    bars = plt.barh(top_politicians, top_counts, color='skyblue')
    
    plt.xlabel('Number of Votes')
    plt.title('Top 20 Vote Counts per Politician')
    
    # Set x-axis limits for zooming in
    plt.xlim(0, max(top_counts) * 0.75)  # Zoom in to 75% of the max count
    
    plt.gca().invert_yaxis()  # Invert y-axis to show the highest votes on top
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
    
    # plot_vote_counts(politician_number_of_votes)

    print(len(politician_number_of_votes))

    print(f'Average length: {float(total_length/document_count)}')
    print(f'Number of documents: {document_count}')
    


   
if __name__ == "__main__":
    main()


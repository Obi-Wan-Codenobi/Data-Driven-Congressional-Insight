import os
from dotenv import load_dotenv
import json
import threading
import time
import matplotlib.pyplot as plt
import xmltodict
import zipfile

load_dotenv()

politician_number_of_votes = {}
lock = threading.Lock()

document_count = 0
total_length = 0
document_lock = threading.Lock()

def start_thread(dir):
    try:
        if os.path.exists(dir):
            
            directories = get_directories(dir)           
        else:
            print(f"Directory does not exist: {dir}")
            
        for path in directories:
              
            # if zip:
            
            # if xml:
            
            # if json:
            pass

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

def unzip(zip_file_path):
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall()

def find_all_files(directory):
    file_paths = []
    for root, dirs, files in os.walk(directory):
        zip_files = [file for file in files if file.endswith('.zip')]
        xml_files = [file for file in files if file.endswith('.xml')]
        json_files = [file for file in files if file.endswith('.json')]
        
        if len(zip_files) > 0 and len(dirs)==0:
            with zipfile.ZipFile(os.path.join(root, zip_files[0]), 'r') as zip_ref:
                zip_ref.extractall()
            unzipped_directories = get_directories(root)
            for dir in unzipped_directories:
                file_paths.extend(find_all_files(os.path.join(root, dir)))
        elif len(xml_files)> 0 and len(dirs)==0:
            for file in xml_files:
                with open(os.path.join(root, dir), 'r') as file:
                    xml_data = file.read()
                    xml_dict = xmltodict.parse(xml_data)
            
            
        elif len(zip_files) > 0 and len(other_files) > 0: # just add all directories anyway? It should not depend
        
            for dir in dirs:
                dir_path = os.path.join(root, dir)
                file_paths.extend(find_all_files(dir_path))  # Recursively search subdir
        else:
            # if no zip files (base case)
            for file in other_files:
                file_paths.append(os.path.join(root, file))
                
    return file_paths

def parseXMLBills(path):
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
    
    with open('data.xml', 'r') as file:
        xml_data = file.read()

    # write to json for future use
    dict_data = xmltodict.parse(xml_data)
    json_data = json.dumps(dict_data, indent=4)

    return dict(vote_count) 

def get_directories(dir):
    directories = []
    for item in os.listdir(dir):
        if os.path.isdir(os.path.join(dir, item)):
            directories.append(os.path.join(dir, item))
    return directories
    


def load_bill_data(file_prefix:str):
    bills_data = get_directories(file_prefix)
    
    threads = []
    for i in bills_data:  
        thread = threading.Thread(target=start_thread, args=(i,))
        threads.append(thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    print("Final count of votes per politician:")
    for politician, count in politician_number_of_votes.items():
        print(f"{politician}: {count}")
    


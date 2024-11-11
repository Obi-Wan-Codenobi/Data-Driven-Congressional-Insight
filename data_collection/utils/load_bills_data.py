import os
from dotenv import load_dotenv
import threading
import zipfile
import datetime
import re
from typing import Dict

class xml_file:
    def __init__(self, file_path, date):
        self.file_path = file_path
        self.date = date
    
load_dotenv()

bills: Dict[str, xml_file] = {}
lock = threading.Lock()

total_document_count = 0
total_document_unique_count = 0
document_count_lock = threading.Lock()

def start_thread(dir):
    try:
        if os.path.exists(dir):
            
            directories = get_directories(dir)           
        else:
            print(f"Directory does not exist: {dir}")
            return
         
        doc_count =0
        doc_unique_count =0
        for path in directories:
            dc , duc = find_all_files(path)
            doc_count+=dc
            doc_unique_count +=duc
            
        with document_count_lock:
            global total_document_count
            global total_document_unique_count
            total_document_count+= doc_count
            total_document_unique_count+= doc_unique_count


    except Exception as e:
        print(f"Error in thread for {dir}: {e}")

def merge_dictionaries(original_dict, new_dict):
    with lock:         
        for key, value in new_dict.items():
            original_dict[key] = original_dict.get(key, 0) + value


def find_all_files(directory):
    file_count = 0
    file_unique = 0
    for root, dirs, files in os.walk(directory):
        zip_files = [file for file in files if file.endswith('.zip')]
        xml_files = [file for file in files if file.endswith('.xml')]
        
        if len(zip_files) > 0 and len(dirs)==0:
            with zipfile.ZipFile(os.path.join(root, zip_files[0]), 'r') as zip_ref:
                zip_ref.extractall(root)
            unzipped_directories = get_directories(root)
            for dir in unzipped_directories:
                tmp_file_count, tmp_file_unique = find_all_files(os.path.join(root, dir))
                file_count += tmp_file_count
                file_unique += tmp_file_unique
                
        elif len(xml_files)> 0 and len(dirs)==0:
            for file in xml_files:
                xml_path = os.path.join(root, file)
                if(parse_XML_bills(xml_path)):
                    file_unique+=1
                file_count+=1
            
        elif len(dirs) > 0:
            for dir in dirs:
                dir_path = os.path.join(root, dir)
                tmp_file_count, tmp_file_unique = find_all_files(dir_path)  # Recursively search subdir
                file_count += tmp_file_count
                file_unique += tmp_file_unique
                
    return file_count, file_unique

 
def get_date_from_regex(date_regex):
    if date_regex is None:
        return None
    date_str = date_regex.group(1)
    if len(date_str)==0:
        return None
    return date_str

def parse_XML_bills(path):
    try:
        with open(path, 'r') as file:
            xml_data = file.read()
            
            title_regex = re.search(r"<dc:title>(.*?)</dc:title>", xml_data)
                            
            if title_regex is None:
                print(f"No title found for {path}")
                return False
 
            title = title_regex.group(1)
            if len(title) == 0:
                title = None

            date_regex = re.search(r"<dc:date>(.*?)</dc:date>", xml_data)
            date_str = get_date_from_regex(date_regex)

            if not date_str:
                date_regex = re.search(r'<action-date(.*?)>(.*?)</action-date>', xml_data)
                date_str = get_date_from_regex(date_regex)
 
            if not date_str:
                date_regex = re.search(r'<action-date".*?">(.*?)</action-date>', xml_data)   
                date_str = get_date_from_regex(date_regex) 

            if not date_str:
                date_regex = re.search(r'(?i)<attestation-date[^>]*>.*?(\b(?:January|February|March|April|May|June|July|August|September|October|November|December) \d{1,2}, \d{4})\b.*?<\/attestation-date>', xml_data)   
                date_str = get_date_from_regex(date_regex)  
            
            if not date_str:
                print(f"No date found for {path}")
                return False 

            try:
                date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
            except ValueError as e:
                print(f"No date found for {path}")
                return False 
                
            if title is None:
                print(f"No title found for {path}")
                return False

            new_xml_file = xml_file(path, date)
            with lock:
                if title in bills:
                    other_xml_file = bills.get(title)
                    
                    if title and date and date > other_xml_file.date:
                        bills[title] = new_xml_file
                        return True
                else:
                    bills[title] = new_xml_file
                    return True
                
    except Exception as e:
        print(f"Error for XML file ({path}): {e}")
        raise TypeError (e)
            
    return False
                    

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

    # print("Final count of bills:")
    # for title, xmlfiles in bills.items():
    #     print(f"{title}: {xmlfiles}")
    print(f'TOTAL DOC COUNT: {total_document_count}')
    print(f'UNIQUE DOC COUNT: {total_document_unique_count}')
    print(f'TOTAL NUMBER OF DOCS IN BILLS: {len(bills)}')
    
    return bills


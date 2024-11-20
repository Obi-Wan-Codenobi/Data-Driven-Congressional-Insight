import os
import threading
import zipfile
import datetime
import re
from typing import Dict
import time

class Bill_file:
    def __init__(self, title: str | None, file_path, date: str | None, ):
        self.title = title
        self.file_path = file_path
        self.date = date

class Load_bills:
    def __init__(self):
        self.bills = {}
        self.errors = {}
        self.lock = threading.Lock()
        self.errors_lock = threading.Lock()
        #self.file_lock = threading.Lock()
    
    # bills = {}
    # errors = {}
    # lock = threading.Lock()
    # errors_lock = threading.Lock()
        

    def start_thread(self,dir):
        try:
            if os.path.exists(dir):
                directories = get_directories(dir)           
            else:
                print(f"Directory does not exist: {dir}")
                return
            
            for path in directories:
                self.find_all_files(path)

        except Exception as e:
            print(f"Error in thread for {dir}: {e}")


    def find_all_files(self, directory):
        for root, dirs, files in os.walk(directory):
            zip_files = [file for file in files if file.endswith('.zip')]
            xml_files = [file for file in files if file.endswith('.xml')]
            
            if len(zip_files) > 0 and len(dirs)==0:
                with zipfile.ZipFile(os.path.join(root, zip_files[0]), 'r') as zip_ref:
                    zip_ref.extractall(root)
                unzipped_directories = get_directories(root)
                for dir in unzipped_directories:
                    self.find_all_files(os.path.join(root, dir))
                    
            elif len(xml_files)> 0 and len(dirs)==0:
                for file in xml_files:
                    xml_path = os.path.join(root, file)
                    self.parse_XML_bills(xml_path)
                
            elif len(dirs) > 0:
                for dir in dirs:
                    dir_path = os.path.join(root, dir)
                    self.find_all_files(dir_path)  # Recursively search subdir

    
    def get_date_from_regex(self, date_regex):
        if date_regex is None:
            return None
        
        last_group_index = date_regex.lastindex
        date_str = date_regex.group(last_group_index)
        if len(date_str)==0:
            return None
        return date_str

    def parse_XML_bills(self, path):
        title = None
        date = None
        try:
            bill_name_regex = re.search(r"/bills/(s|hr)/(.*?)/xml/(.*?)(\d+[a-zA-Z]\d+).*?.xml", str(path))
            if not bill_name_regex:
                bill_name_regex = re.search(r"xml/(.*?).xml", str(path))
            if bill_name_regex is None:
                return False
            bill_name = self.get_date_from_regex(bill_name_regex)
            
            
            # with self.file_lock:
            #     with open(path, 'r') as file:
            #         xml_data = file.read()

            with open(path, 'r') as file:
                xml_data = file.read()

                
            title_regex = re.search(r"<dc:title>(.*?)</dc:title>", xml_data)
            if title_regex:
                title = title_regex.group(1)
    

            date_regex = re.search(r"<dc:date>(.*?)</dc:date>", xml_data)
            date_str = self.get_date_from_regex(date_regex)

            if not date_str:
                date_regex = re.search(r'<action-date[^>]*>(.*?(\w+\s\d{1,2},\s\d{4}))</action-date>', xml_data)
                date_str = self.get_date_from_regex(date_regex)

            if not date_str:
                date_regex = re.search(r'<action-date".*?">(.*?)</action-date>', xml_data)   
                date_str = self.get_date_from_regex(date_regex) 

            if not date_str:
                date_regex = re.search(r'(?i)<attestation-date[^>]*>.*?(\b(?:January|February|March|April|May|June|July|August|September|October|November|December) \d{1,2}, \d{4})\b.*?<\/attestation-date>', xml_data)   
                date_str = self.get_date_from_regex(date_regex)  
            
            if not date_str:
                date_regex = re.search(r'<attestation-date(.*?)>(.*?)</attestation-date>', xml_data)   
                date_str = self.get_date_from_regex(date_regex)  
                
                if date_str:
                    date_match = re.search(r'(\w+\s\d{1,2},\s\d{4})', date_str)
                    date_str = self.get_date_from_regex(date_match)
            
            if not date_str:
                date_regex = re.search(r'<action-date>(\w+\s\d{1,2},\s\d{4})</action-date>', xml_data)   
                date_str = self.get_date_from_regex(date_regex) 
                
            if date_str:
                date_formats = [
                    "%Y-%m-%d", 
                    "%B %d, %Y", 
                    "(%B %d, %Y)"  
                ]
                date = None
                for date_format in date_formats:
                    try:
                        date = datetime.datetime.strptime(date_str, date_format)
                        break
                    except ValueError:
                        date = None
                        continue
                
            else:
                date = "n/a"
                error_msg = f"No date ({date_str}) found for {path}"
                with self.errors_lock:
                    self.errors[bill_name] = error_msg

                
            if title is None:
                title = "n/a"
                error_msg = f"No title found for {path}"
                with self.errors_lock:
                    self.errors[bill_name] = error_msg


            new_bill_file = Bill_file(title, path, date)
            with self.lock:
                if bill_name not in self.bills:
                    self.bills[bill_name] = new_bill_file
                    return True
                    
        except Exception as e:
            print(f"Error for XML file ({path}): {e}")
            raise TypeError (e)
                
        return False
                        


        


    def fetch(self, file_prefix:str):

        bills_data = get_directories(file_prefix)
        threads = []
        for i in bills_data:  
            thread = threading.Thread(target=self.start_thread, args=(i,))
            threads.append(thread)

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        
        # with self.errors_lock:
        #     for bill, error in self.errors.items():
        #         print(f"Bill {bill} : error {error}")
        
        return self.bills
    
def get_directories(dir):
        directories = []
        for item in os.listdir(dir):
            if os.path.isdir(os.path.join(dir, item)):
                directories.append(os.path.join(dir, item))
        return directories

def load_and_merge_all_bills(directories):
    start = time.time()
    merged_data = {}
    lock = threading.Lock()
    
    # sub_directories = []
    # for dir in directories:
    #     print(dir)
    #     if os.path.exists(dir):
    #         sub_directories.extend(get_directories(dir))
    # print(sub_directories)
  
    def load_data_for_directory(directory):
        loader = Load_bills()
        data = loader.fetch(directory)
        with lock:
            merged_data.update(data)
            print(f"{len(data)} Bills found for {directory}")

    threads = []

    # new thread for each congress session
    for dir in directories:
        thread = threading.Thread(target=load_data_for_directory, args=(dir,))
        thread.start()
        threads.append(thread)


    for thread in threads:
        thread.join()
    end = time.time()

    print(f"{len(merged_data)} Bills found total")
    print(f"Time elasped: {float((end-start)/60)} minutes")
    print(f"Time elasped: {float((end-start))} seconds")
    return merged_data
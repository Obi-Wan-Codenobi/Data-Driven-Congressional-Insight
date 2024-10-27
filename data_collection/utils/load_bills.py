import requests
import os
import json
import xml.etree.ElementTree as ET
from dotenv import load_dotenv

load_dotenv()

#
# This document encases all functions needed
#


#requests data from the api
def fetch_data(api_url):
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"Error: Received response code {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

#saves url files to bill_files
def save_xml_to_file(url, file_path):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(file_path, 'wb') as file:
                file.write(response.content)
            
        else:
            print(f"Error: Could not fetch XML from {url}. Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred while saving XML: {e}")

#finds .xml url in the folder bill_urls to that the contents can be dropped into bill_texts
# used in save_bill_texts
def extract_xml_urls_from_folder(output_folder):
    bill_urls = []
    for file_name in os.listdir(output_folder):
        if file_name.endswith('.xml'):
            
            bill_number = file_name.split('_')[1].replace('.xml', '')
            
            xml_url = f'https://www.congress.gov/117/bills/hr{bill_number}/BILLS-117hr{bill_number}ih.xml'
            bill_urls.append(xml_url)
    return bill_urls

#takes a list of .xml text files and their desired folder and stored the content of those links in those files
def save_bill_texts(xml_urls, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    for xml_url in xml_urls:
        
        try:
            
            response = requests.get(xml_url)
            response.raise_for_status()
            xml_content = response.content
            
            
            root = ET.fromstring(xml_content)
            bill_text = ET.tostring(root, encoding='unicode', method='text')

            
            bill_number = xml_url.split('/')[-1].split('hr')[1][:4]  
             
            

            file_name = f"Bill{bill_number}_text.txt"
            file_path = os.path.join(output_folder, file_name)

            

            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(bill_text)

            #print(f"Saved: {file_path}")
        except requests.HTTPError as e:
            print(f"Error fetching XML from {xml_url}. Status code: {e.response.status_code}")
        except ET.ParseError as e:
            print(f"Error parsing XML from {xml_url}: {e}")
        except Exception as e:
            print(f"An error occurred while processing the XML: {e}")
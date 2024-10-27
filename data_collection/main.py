import requests
import os
import json
import xml.etree.ElementTree as ET
from dotenv import load_dotenv

load_dotenv()


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

            sections = bill_text.split('.')  
            formatted_text = '\n\n'.join(section.strip() for section in sections)

            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(formatted_text)

            #print(f"Saved: {file_path}")
        except requests.HTTPError as e:
            print(f"Error fetching XML from {xml_url}. Status code: {e.response.status_code}")
        except ET.ParseError as e:
            print(f"Error parsing XML from {xml_url}: {e}")
        except Exception as e:
            print(f"An error occurred while processing the XML: {e}")

def main():
    api_key = os.getenv("API_KEY")
    base_url = "https://api.congress.gov/v3/bill/117"
    output_folder = "bill_urls"
    output_folder2 = "bill_texts"
    os.makedirs(output_folder, exist_ok=True)

    
    bills_url = f'{base_url}?fromDateTime=2021-01-01T00:00:00Z&toDateTime=2022-12-31T23:59:59Z&sort=updateDate+desc&api_key={api_key}'
    
    bills_data = fetch_data(bills_url)
    
    
    if bills_data and "bills" in bills_data:
        bill_urls = [] 
        bill_nums = []
        for bill in bills_data["bills"]:
            bill_number = bill["number"]
            bill_congress = bill["congress"]
            bill_type = bill["type"].lower()
            
            #print(f"Processing bill: Congress {bill_congress}, Type {bill_type}, Number {bill_number}")

            bill_text_url = f'https://api.congress.gov/v3/bill/{bill_congress}/{bill_type}/{bill_number}/text?api_key={api_key}'
            file_path = os.path.join(output_folder, f"Bill_{bill_number}.xml")
            
            save_xml_to_file(bill_text_url, file_path)


        bill_urls = extract_xml_urls_from_folder(output_folder)
        save_bill_texts(bill_urls, output_folder2)
    else:
        print("No bills data found.")

if __name__ == "__main__":
    main()

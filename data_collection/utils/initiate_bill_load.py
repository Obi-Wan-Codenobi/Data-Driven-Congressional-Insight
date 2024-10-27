from utils.load_bills import *


def initiate_bill_load():

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

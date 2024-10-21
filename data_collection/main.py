
import requests
import os
from dotenv import load_dotenv
import json

load_dotenv()

'''
Get cosponsors:
    
    GET /bill/:congress/:billType/:billNumber/cosponsors
    Example Request
    https://api.congress.gov/v3/bill/117/hr/3076/cosponsors?api_key=[INSERT_KEY]
    
    GET /amendment/:congress/:amendmentType/:amendmentNumber/cosponsors
    Example Request
    https://api.congress.gov/v3/amendment/117/samdt/2137/cosponsors?api_key=[INSERT_KEY]
'''
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

def main():
    api_key = os.getenv("API_KEY")
    #api_url = f'https://api.congress.gov/v3/bill?api_key={api_key}'
    api_url = f'https://api.congress.gov/v3/bill/117?fromDateTime=2000-08-04T04:02:00Z&toDateTime=2000-09-30T04:03:00Z&sort=updateDate+desc&api_key={api_key}'

    print(api_url)

    data = fetch_data(api_url)

    if data:
        file_name = "data_dump.txt"
        opened_file = open(file_name , "w")

        print(json.dumps(data, indent=4), file=opened_file)

if __name__ == "__main__":
    main()


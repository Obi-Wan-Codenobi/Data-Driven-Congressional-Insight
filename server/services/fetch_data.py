import requests
import httpx
import asyncio

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
    
async def fetch_data_async(api_url):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(api_url)
            response.raise_for_status()  
            return response.json()
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
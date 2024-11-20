from .fetch_data import fetch_data
import dotenv 
import os
from data.state_codes import us_state_codes
from .fetch_data import fetch_data_async
import asyncio
import json
dotenv.load_dotenv()

CONGRESS_API_KEY= os.getenv("API_KEY")



async def get_all_politicians():
    tasks = []
    result = []
    for code in us_state_codes:
        query = f"https://api.congress.gov/v3/member/{code}?currentMember=true&api_key={CONGRESS_API_KEY}"
        tasks.append(fetch_data_async(query))
        
    responses = await asyncio.gather(*tasks)
    
    for json in responses:
        if json:
            for member in json.get("members", None):
                result.append(person_card_data(member))

    return result
    
def person_card_data(json_input):
    result = {}
    result["id"] = json_input.get("bioguideId", None)
    result["name"] = json_input.get("name", None)
    result["image_url"] = json_input.get("depiction", {}).get("imageUrl", None)
    result["party"] = json_input.get("partyName", None)
    
    return result
    
from data.topics import political_topics_images
import dotenv
import os

dotenv.load_dotenv()

STATIC_IMAGE_PATH= os.getenv("STATIC_IMAGE_PATH")
DOMAIN_NAME= os.getenv("DOMAIN_NAME")
async def get_all_topics():
    tasks = []
    result = []
    id = 0
    for topic, image_name in political_topics_images.items():
        id+=1
        topic_card = {}
        topic_card["id"] = id
        topic_card["title"] = topic
        topic_card["image_url"] = DOMAIN_NAME +'/' + STATIC_IMAGE_PATH + '/' +image_name
        result.append(topic_card)
    return result
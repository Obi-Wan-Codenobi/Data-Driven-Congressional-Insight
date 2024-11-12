from config.bm25 import query_bm25, top_ten_documents, to_json

async def topic_query(data_json):
    result = query_bm25(data_json["input"])
    documents = top_ten_documents(result)
    json = to_json(result)
    return json
from config.bm25 import query_bm25, top_ten_documents, to_json


def html_page(document):
    return f"""
    <div>
        <h3>{document.title} </h3>
        <p>{document.body} </p>
    <div>
    """
    
async def search_query(data_json):
    result = query_bm25(data_json["input"])
    documents_and_score = top_ten_documents(result)
    json = []
    html = {}
    
    for document in documents_and_score:
        doc = document[0]
        dict_doc = {}
        dict_doc["id"] = doc.id
        dict_doc["title"] = doc.title
        json.append(dict_doc)
        
        html[doc.id] = html_page(doc)
        
    response = {
        "json": json,
        "html_documents": html
    }
    return response
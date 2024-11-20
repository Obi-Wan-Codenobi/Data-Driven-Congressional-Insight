from config.bm25 import document_id_to_vote, query_bm25, top_ten_documents, to_json, votes


document_vote_data = document_id_to_vote()
print(document_vote_data)

def html_page(document):
    return f"""
    <div>
        <h3>{document.title} </h3>
        <p>{document.body} </p>
    <div>
    """

def get_votes(doc_id):
    try:
        key = document_vote_data.get(doc_id)
        if not key:
            print(key)
            return "None"
        
        document_vote = votes.get(key, "None")
        if document_vote != "None":
            print(document_vote)
        return document_vote
    except Exception as e:
        print(f"Could not find vote data for document {doc_id}, Error: {e}")
        return "None"
    
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
        dict_doc["votes"] = get_votes(doc.id)
        json.append(dict_doc)
        
        html[doc.id] = html_page(doc)
        
    response = {
        "json": json,
        "html_documents": html
    }
    return response
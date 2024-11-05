import math
from collections import defaultdict



class BM25:
    def __init__ (self, docs, freq_per_doc, total_number_of_docs, query):
        self.docs = docs
        self.query = query
        self.freq_per_doc = freq_per_doc
        # Weights and parameters 
        # continue to develop as documents grow!!
        self.title_weight = 1.0
        self.body_weight = 0.05
        self.b25title = 0.5
        self.b25body = 0.9
        self.k1 = 2.0
        self.pageRank_lambda = 0.8
        self.pageRank_lambda_prime = 0.9
        self.total_number_of_docs = total_number_of_docs
        # bm25 storages
        self.lengths = {} #used in calc_average_lengths & normalize
        self.avg_lengths = {} 
        self.pagerank_scores = {}
        self
        # Calculate average lengths
        self.calc_average_lengths()



    def calc_average_lengths(self):
        total_title_length = 0.0
        total_body_length = 0.0
        count = 0
        for index, doc in enumerate(self.docs):
                title_length = doc["TITLE_LENGTH"]
                body_length = doc["BODY_LENGTH"]

                self.lengths[index] = {
                    "title": title_length,
                    "body": body_length
                }

                total_title_length += title_length
                total_body_length += body_length
                count += 1

                # PageRank score handling (example logic, modify as needed)
                pagerank_score = self.pageRank_lambda_prime * self.pagerank_scores.get(index, 0.0)
                self.pagerank_scores[index] = pagerank_score

        self.avg_lengths["title"] = total_title_length / count if count > 0 else 0.0
        self.avg_lengths["body"] = total_body_length / count if count > 0 else 0.0


    # TODO 
    #get_num_of docs needs to be filled in
    #get_docs_with_query needs to be filled out
    def get_docs_with_query(self, term):
        count = 0
        for doc in self.docs:
        
            if term in doc["BODY"] or doc["TITLE"]:
                count += 1
        return count
    

    def get_num_of_docs(self):
        return self.total_number_of_docs
    
    def get_idf(self, term):
        docs_containing_terms =  self.get_docs_with_query(term)
        idf = math.log(self.get_num_of_docs() / docs_containing_terms)
        return idf

    def calculate_term_frequencies(self, documents):
        term_frequencies = []
        
        for doc in documents:
            tf = {
                "title": defaultdict(int),  
                "body": defaultdict(int)
            }

            title = doc["TITLE"].lower().split()  
            for term in title:
                tf["title"][term] += 1

            body = doc["BODY"].lower().split()  
            for term in body:
                tf["body"][term] += 1

            term_frequencies.append(tf)
        
        return term_frequencies
    

    def get_net_score(self, tfs, query, tf_query, doc):
        score = 0.0

        for term in query.query_words:
            Wf = self.title_weight if term in tfs.get("title", {}) else self.body_weight
            ftf = (tfs.get("title", {}).get(term, 0.0) + tfs.get("body", {}).get(term, 0.0))
            idf = self.get_idf(term)

            pagerank_score = math.log(1 + self.pagerank_scores.get(doc, 0.0))

            score += (Wf * ftf) / (self.k1 + ftf * Wf) * idf + self.pageRank_lambda * pagerank_score

        return score

    def normalize_tfs(self, tfs, doc, query):
        for tf_type in ["title", "body"]:
            length = self.lengths[doc][tf_type]
            avg_length = self.avg_lengths[tf_type]
            Bf = self.b25title if tf_type == "title" else self.b25body

            for term in tfs.get(tf_type, {}).keys():
                raw_tf = tfs[tf_type][term]
                normalized_tf = raw_tf / ((1 - Bf) + Bf * (length / avg_length))
                tfs[tf_type][term] = normalized_tf

    def score_documents(self):
        scored_docs = []
    
    
        term_frequencies = self.calculate_term_frequencies(self.docs)
        tf_query = defaultdict(int)
        for term in self.query.query_words:
            tf_query[term] += 1
        for index, doc in enumerate(self.docs):
            self.normalize_tfs(term_frequencies[index], index, self.query)  
            score = self.get_net_score(term_frequencies[index], self.query, tf_query, index) 
            scored_docs.append((doc, score))  
        return scored_docs
    

